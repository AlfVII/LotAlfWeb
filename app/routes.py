from flask import render_template, get_template_attribute, redirect, url_for, request, make_response, session
from app import app
from app.forms import NumberForm, PostForm, RetailerForm
from app import local_db
from app import numbers_collection_db
from app import retailers_collection_db
from app import comments_db
import json
import collections
import pandas
import os
import base64
from hashlib import md5


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PostForm()
    comments_db_inst = comments_db.CommentsDB()
    posts = comments_db_inst.get_all_comments().to_dict('records')
    for index, post in enumerate(posts):
        posts[index]['identicon'] = f"https://www.gravatar.com/avatar/{md5(post['name'].encode('utf-8')).hexdigest()}?d=identicon"
    posts.reverse()
    if form.validate_on_submit():
        comments_db_inst.insert_comment(
            name=form.name.data,
            email=form.email.data,
            comment=form.post.data)
        return redirect(url_for('index'))

    return render_template('index.html', title='Home', posts=posts, form=form)


@app.route('/retailers_collection', methods=['GET', 'POST'])
def retailers_collection():
    form = RetailerForm()
    initial_latitude = 40.4169473
    initial_longitude = -3.7035285
    if request.method == 'GET':
        if 'retailer_region' in session:
            del session['retailer_region']
        if 'retailer_province' in session:
            del session['retailer_province']
        if 'retailer_town' in session:
            del session['retailer_town']
    local_db_inst = local_db.LocalDB()

    if session.get('retailer_region') is not None:
        provinces = local_db_inst.get_all_provinces(session.get('retailer_region').upper())
        form.retailer_province.choices = [(province.title(), province.title()) for province in provinces]
    if session.get('retailer_province') is not None:
        towns = local_db_inst.get_all_towns(session.get('retailer_province').upper())
        form.retailer_town.choices = [(town.title(), town.title()) for town in towns]

    if form.validate_on_submit():
        data = form.data
        if os.path.isfile("app/tmp/image.jpg"):
            with open("app/tmp/image.jpg", "rb") as image_file:
                data['image'] = base64.b64encode(image_file.read())
        else:
            data['image'] = None
        retailers_collection_db_inst = retailers_collection_db.RetailersCollectionDB()
        if data['owned'] == "Owned":
            del data['owned']
            del data['submit_save']
            del data['csrf_token']
            retailers_collection_db_inst.update_retailer(data)
            data['owned'] = "Owned"
        else:
            retailers_collection_db_inst.delete_retailer(data)
        retailers_collection_db_inst.close_connection()

        retailers = pandas.DataFrame(data, index=[0], columns=["id", "retailer_number", "retailer_street", "retailer_street_number", "retailer_postal_code", "retailer_town", "retailer_telephone", "retailer_longitude", "retailer_latitude", "retailer_province", "retailer_region", "number"])
        retailers = retailers.set_index("id")
        return render_template('retailers_collection.html', form=form, latitude=initial_latitude, longitude=initial_longitude, markers=create_marker(retailers, data['owned'] == "Owned"))
    else:
        return render_template('retailers_collection.html', form=form, latitude=initial_latitude, longitude=initial_longitude, markers='')


def create_marker(retailers, owned):
    opt_owned = """{
                iconCreateFunction: function (cluster) {
                    var childCount = cluster.getChildCount();

                    var c = ' marker-cluster-owned-';
                    if (childCount < 10) {
                        c += 'small';
                    } else if (childCount < 100) {
                        c += 'medium';
                    } else {
                        c += 'large';
                    }

                    return new L.DivIcon({ html: '<div><span>' + childCount + '</span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });
                }
            }"""

    markers = f"""var markerClusters_{owned} = L.markerClusterGroup({opt_owned if owned else ''});"""
    for row_index, row in retailers.iterrows():
        if owned:
            icon = "{icon: my_marker_own}"
        else:
            icon = "{icon: my_marker_not}"
        markers += f"var _{row_index} = L.marker([{row['retailer_latitude']}, {row['retailer_longitude']}], {icon});\
                     _{row_index}.on('click', click_on_marker).bindPopup('{row['retailer_region']}<br>{row['retailer_province']}<br>{row['retailer_town']}<br>{row['retailer_number']}<br>{row['retailer_street']}<br>{row['retailer_street_number']}<br>{row['retailer_postal_code']}<br>{row['retailer_telephone']}<br>{row['number']}');\
                     markerClusters_{owned}.addLayer( _{row_index} );"
    markers += f"map.addLayer( markerClusters_{owned} );"

    return markers


@app.route('/get_retailer_data', methods=['GET', 'POST'])
def get_retailer_data():
    if request.method == 'POST':
        retailers_collection_db_inst = retailers_collection_db.RetailersCollectionDB()
        local_db_inst = local_db.LocalDB()
        owned_retailers = retailers_collection_db_inst.get_retailers(['retailer_province', 'retailer_town', 'retailer_number'], [request.form['retailer_province'], request.form['retailer_town'], request.form['retailer_number']])
        retailers = local_db_inst.get_retailers(['retailer_province', 'retailer_town', 'retailer_number'], [request.form['retailer_province'].upper(), request.form['retailer_town'].upper(), request.form['retailer_number'].upper()])
        retailers_collection_db_inst.close_connection()
        if len(owned_retailers) == 0:
            if len(retailers) != 0:
                retailers = pandas.DataFrame(retailers, columns=["id", "retailer_number", "retailer_street", "retailer_street_number", "retailer_postal_code", "retailer_town", "retailer_telephone", "retailer_longitude", "retailer_latitude", "retailer_province", "retailer_region"])
                return make_response(json.dumps(retailers.iloc[0].to_dict()))
            else:
                return make_response(json.dumps(None))
        else:
            owned_retailers = pandas.DataFrame(owned_retailers, columns=["id", "retailer_number", "retailer_street", "retailer_street_number", "retailer_postal_code", "retailer_town", "retailer_telephone", "retailer_longitude", "retailer_latitude", "retailer_province", "retailer_region"])
            return make_response(json.dumps(owned_retailers.iloc[0].to_dict()))


@app.route('/update_map', methods=['GET', 'POST'])
def update_map():
    initial_latitude = 40.4169473
    initial_longitude = -3.7035285
    local_db_inst = local_db.LocalDB()
    retailers_collection_db_inst = retailers_collection_db.RetailersCollectionDB()
    if request.method == 'POST':
        if 'all_retailers' in request.form and request.form['all_retailers'] == 'true':
            retailers = local_db_inst.get_all_retailers()
            owned_retailers = retailers_collection_db_inst.get_all_retailers()
        elif 'all_owned_retailers' in request.form and request.form['all_owned_retailers'] == 'true':
            retailers = []
            owned_retailers = retailers_collection_db_inst.get_all_retailers()
        elif request.form['retailer_town'] != '' and 'retailer_province' not in request.form:
            retailers = local_db_inst.get_retailers_like(['retailer_town'], [request.form['retailer_town'].upper()])
            owned_retailers = retailers_collection_db_inst.get_retailers_like(['retailer_town'], [request.form['retailer_town']])
        elif request.form['retailer_number'] != '' and 'retailer_province' not in request.form:
            retailers = local_db_inst.get_retailers(['retailer_number'], [request.form['retailer_number'].upper()])
            owned_retailers = retailers_collection_db_inst.get_retailers(['retailer_number'], [request.form['retailer_number']])
        elif request.form['retailer_region'] != '' and request.form['retailer_province'] == '':
            retailers = local_db_inst.get_retailers(['retailer_region'], [request.form['retailer_region'].upper()])
            owned_retailers = retailers_collection_db_inst.get_retailers(['retailer_region'], [request.form['retailer_region']])
        elif request.form['retailer_province'] != '' and request.form['retailer_town'] == '':
            retailers = local_db_inst.get_retailers(['retailer_province'], [request.form['retailer_province'].upper()])
            owned_retailers = retailers_collection_db_inst.get_retailers(['retailer_province'], [request.form['retailer_province']])
        elif request.form['retailer_town'] != '' and request.form['retailer_number'] == '':
            retailers = local_db_inst.get_retailers(['retailer_province', 'retailer_town'], [request.form['retailer_province'].upper(), request.form['retailer_town'].upper()])
            owned_retailers = retailers_collection_db_inst.get_retailers(['retailer_province', 'retailer_town'], [request.form['retailer_province'], request.form['retailer_town']])
        elif request.form['retailer_town'] != '' and request.form['retailer_number'] != '':
            retailers = local_db_inst.get_retailers(['retailer_province', 'retailer_town', 'retailer_number'], [request.form['retailer_province'].upper(), request.form['retailer_town'].upper(), request.form['retailer_number'].upper()])
            owned_retailers = retailers_collection_db_inst.get_retailers(['retailer_province', 'retailer_town', 'retailer_number'], [request.form['retailer_province'], request.form['retailer_town'], request.form['retailer_number']])

    retailers_collection_db_inst.close_connection()
    retailers = pandas.DataFrame(retailers, columns=["id", "retailer_number", "retailer_street", "retailer_street_number", "retailer_postal_code", "retailer_town", "retailer_telephone", "retailer_longitude", "retailer_latitude", "retailer_province", "retailer_region"])
    retailers[["retailer_street", "retailer_street_number", "retailer_town", "retailer_province", "retailer_region"]] = retailers[["retailer_street", "retailer_street_number", "retailer_town", "retailer_province", "retailer_region"]].apply(lambda column: column.str.title())
    retailers = retailers.set_index(['retailer_province', 'retailer_town', 'retailer_number'])
    owned_retailers = owned_retailers.set_index(['retailer_province', 'retailer_town', 'retailer_number'])
    retailers['number'] = None

    if not retailers.empty:
        retailers.update(owned_retailers)
    else:
        retailers = owned_retailers

    retailers = retailers.convert_dtypes()

    retailers = retailers.reset_index().set_index("id")
    map = get_template_attribute("map.html", "insert_map")
    if not retailers.empty:
        # retailers["number"] = retailers.apply(lambda row: "69" if row['retailer_region'] == 'Comunidad De Madrid' else row["number"], axis=1)

        markers = create_marker(retailers[retailers['number'].notnull()], True)
        markers += create_marker(retailers[retailers['number'].isnull()], False)
        return map(retailers['retailer_latitude'].mean(), retailers['retailer_longitude'].mean(), markers)
    else:
        return map(initial_latitude, initial_longitude)


@app.route('/numbers_collection', methods=['GET', 'POST'])
def numbers_collection():
    current_number = 00000
    form = NumberForm()
    local_db_inst = local_db.LocalDB()
    if session.get('retailer_region') is not None:
        provinces = local_db_inst.get_all_provinces(session.get('retailer_region').upper())
        form.retailer_province.choices = [(province.title(), province.title()) for province in provinces]
    if session.get('retailer_province') is not None:
        towns = local_db_inst.get_all_towns(session.get('retailer_province').upper())
        form.retailer_town.choices = [(town.title(), town.title()) for town in towns]
    if session.get('current_number') is not None:
        current_number = int(session.get('current_number'))

    if form.validate_on_submit():
        numbers_collection_db_inst = numbers_collection_db.NumbersCollectionDB()
        datum = {
            'status': form.status.data,
            'origin': form.origin.data,
            'lot': form.lot.data,
            'year': form.year.data,
            'coin': form.coin.data,
            'retailer_region': form.retailer_region.data,
            'retailer_province': form.retailer_province.data,
            'retailer_town': form.retailer_town.data,
            'retailer_number': form.retailer_number.data,
            'copies': form.copies.data
        }
        keys_to_delete = []
        for k, v in datum.items():
            if v == 'Default':
                keys_to_delete.append(k)
        for k in keys_to_delete:
            del datum[k]

        numbers_collection_db_inst.update_number(session['current_number'], datum)
    return render_template('numbers_collection.html', current_number=current_number, form=form)


@app.route('/update_session', methods=['POST'])
def update_session():
    session[request.form['key']] = request.form['value']
    return request.form


@app.route('/get_number', methods=['POST'])
def get_number():
    session['current_number'] = request.form['new_number']
    numbers_collection_db_inst = numbers_collection_db.NumbersCollectionDB()
    number_data = numbers_collection_db_inst.get_number(request.form['new_number'])
    response = make_response(json.dumps(number_data.iloc[0].to_dict()))
    return response


@app.route('/update_provinces', methods=['POST'])
def update_provinces():
    local_db_inst = local_db.LocalDB()
    provinces = local_db_inst.get_all_provinces(request.form['new_region'].upper())
    response = make_response(json.dumps(provinces))
    response.content_type = 'application/jsons'
    return response


@app.route('/update_towns', methods=['POST'])
def update_towns():
    local_db_inst = local_db.LocalDB()
    provinces = local_db_inst.get_all_towns(request.form['new_province'].upper())
    response = make_response(json.dumps(provinces))
    response.content_type = 'application/jsons'
    return response


@app.route('/get_existing_in_hundred', methods=['POST'])
def get_existing_in_hundred():
    numbers_collection_db_inst = numbers_collection_db.NumbersCollectionDB()
    hundred = numbers_collection_db_inst.get_hundred(request.form['number'])
    response = make_response(json.dumps(hundred['status'].to_list()))
    response.content_type = 'application/jsons'
    return response


@app.route('/store_image', methods=['POST'])
def store_image():
    image = request.form['image']
    prefix = 'data:image/webp;base64,'
    cut_image = image[len(prefix):]
    imgdata = base64.b64decode(cut_image)
    filename = 'app/tmp/image.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)
    response = make_response(json.dumps(True))
    response.content_type = 'application/jsons'
    return response


@app.route('/load_image', methods=['POST'])
def load_image():
    retailers_collection_db_inst = retailers_collection_db.RetailersCollectionDB()
    owned_retailers = retailers_collection_db_inst.get_retailers(['retailer_province', 'retailer_town', 'retailer_number'], [request.form['retailer_province'], request.form['retailer_town'], request.form['retailer_number']])
    retailers_collection_db_inst.close_connection()
    if owned_retailers.empty or owned_retailers['image'].iloc[0] is None:
        return ''

    image = bytes(owned_retailers['image'].iloc[0]).decode("utf-8")
    response = make_response(image)
    response.content_type = 'application/jsons'
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form['password'] == 'asd':
        session['logged_in'] = True
    return request.referrer.split('/')[-1]


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del session['logged_in']
    return request.referrer.split('/')[-1]


@app.route('/check_login', methods=['GET', 'POST'])
def check_login():
    if 'logged_in' in session:
        return "logged in"
    else:
        return "not logged in"


@app.route('/numbers_statistics', methods=['GET', 'POST'])
def numbers_statistics():
    return render_template('numbers_statistics.html')


@app.route('/retailers_statistics', methods=['GET', 'POST'])
def retailers_statistics():
    return render_template('retailers_statistics.html')


def get_count(data, column):
    aux = data.value_counts(subset=[column])
    aux = aux.rename({'': "Sin datos"})
    aux = aux.sort_values(ascending=False)
    datum = collections.OrderedDict()
    for k, v in aux.iteritems():
        if k[0] != "Sin datos":
            if isinstance(k[0], str):
                datum[k[0].title()] = v
            else:
                datum[int(k[0])] = v
    return datum


@app.route('/get_numbers_statistics', methods=['GET', 'POST'])
def get_numbers_statistics():

    numbers_collection_db_inst = numbers_collection_db.NumbersCollectionDB()
    numbers_collection = numbers_collection_db_inst.get_all_numbers()
    data = {}

    aux = numbers_collection.value_counts(subset=['status'])
    data['numbers_statuses'] = {}
    for k, v in aux.iteritems():
        data['numbers_statuses'][k[0]] = v

    data['numbers_regions'] = get_count(numbers_collection, 'retailer_region')
    data['numbers_provinces'] = get_count(numbers_collection, 'retailer_province')
    data['numbers_years'] = get_count(numbers_collection, 'year')
    data['numbers_origins'] = get_count(numbers_collection, 'origin')
    data['numbers_coins'] = get_count(numbers_collection, 'coin')

    data['numbers_filled'] = collections.OrderedDict()
    data['numbers_filled']['Por rellenar'] = len(numbers_collection[(numbers_collection['retailer_province'].isnull()) | (numbers_collection['retailer_province'] == '')].index)
    data['numbers_filled']['Rellenados'] = len(numbers_collection[(numbers_collection['retailer_province'].notnull()) & (numbers_collection['retailer_province'] != '')].index)

    return make_response(json.dumps(data))


@app.route('/get_retailers_statistics', methods=['GET', 'POST'])
def get_retailers_statistics():
    local_db_inst = local_db.LocalDB()
    retailers_collection_db_inst = retailers_collection_db.RetailersCollectionDB()
    retailers_collection = retailers_collection_db_inst.get_all_retailers()

    data = {}

    data['retailers_regions'] = get_count(retailers_collection, 'retailer_region')
    data['retailers_provinces'] = get_count(retailers_collection, 'retailer_province')

    data['retailers_filled'] = collections.OrderedDict()
    data['retailers_filled']['Por rellenar'] = local_db_inst.get_retailers_count()
    data['retailers_filled']['Rellenados'] = len(retailers_collection.index)

    data['retailers_with_image'] = collections.OrderedDict()
    data['retailers_with_image']['Con imagen'] = len(retailers_collection[retailers_collection['image'].notnull()].index)
    data['retailers_with_image']['Sin imagen'] = len(retailers_collection[retailers_collection['image'].isnull()].index)

    return make_response(json.dumps(data))
