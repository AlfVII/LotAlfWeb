function pad(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}

function resize_buttons() {
    if ($(window).width() < 1000) {
        $(".group_label").css("font-size", 12);
        $(".btn_number").removeClass('btn-lg').removeClass('btn-md').removeClass('btn-sm').addClass('btn-sm');
    }
    else if ($(window).width() < 1250) {
        $(".group_label").css("font-size", 14);
        $(".btn_number").removeClass('btn-lg').removeClass('btn-md').removeClass('btn-sm').addClass('btn-md');
    }
    else {
        $(".group_label").css("font-size", 19);
        $(".btn_number").removeClass('btn-lg').removeClass('btn-md').removeClass('btn-sm').addClass('btn-lg');
    }
}

var update_number_enabled = true;
var update_colors_enabled = true;

function get_filtered_list() {
    var filters = []
    $(`.slider_filter`).each(function(index) {
        var name = $(this).attr("name").split("slider_filter_")[1]
        filled_filter = $(this).val();
        use = (filled_filter == 0) | (filled_filter != 0 & $(`#filter_${name}`).val() != '');
        if (use) {
            filter = {"name": name, "filled": filled_filter, "value": $(`#filter_${name}`).val()}
            filters.push(filter)
        }
    });
    console.log(filters);
    $("#filtered_list").html(('<img class="loading" src="./static/loading.gif">'))
    limit = $("#filter_limit").val();

    $.post('/get_filtered_numbers', {
        filters: JSON.stringify(filters),
        limit: limit,
    }).done(function(response) {
        response = JSON.parse(response)
        console.log(response)

        html = ''
        response.forEach(function callback(number) {
            html += `<button type="button" onclick="update_number(0, ${number})" class="btn_number btn btn-lg btn-secondary ml-1 mb-1" name="button_number_${number}">${number}</button>`
        });
        $("#filtered_list").html(html)

    }).fail(function() {
        $("#hundred_container").html("Error getting existing for " + filters);
    });
}


function add_filter(name, label) {
        return `<div class="form-inline">
            <div class="input-group-prepend">
                <span class="input-group-text mx-2" style="width:120px">${label}</span>
                <span class="text mx-2 ">¿Rell.?</span>
                <span class="text mx-2 ">No</span>
            </div>
            <input type="range" class="slider_filter" id="slider_filter_${name}" name="slider_filter_${name}" style="width:40px" min="0" max="1" value="1"}>
            <div class="input-group-append">
                <span class="text ml-2 mr-3">Sí</span>
            </div>

            <input type="text" style="text-align:right; width:150px;" class="form-control" id="filter_${name}" name="filter[${name}]">
        </div>`
    }


function update_colors(number) {
    if (update_colors_enabled) {
        update_colors_enabled = false;
        var button_html = $("#hundred_container").html();
        $("#hundred_container").html('<img class="loading" src="./static/loading.gif">');
        $.post('/get_existing_in_hundred', {
            number: number - (number % 100)
        }).done(function(response) {
            $("#hundred_container").html(button_html);
            response = JSON.parse(response)

            for (var i = 0; i < response.length; i++){
                $("#button_number_" + pad(i, 2)).removeClass('btn-success ').removeClass('btn-secondary ').removeClass('btn-warning ').removeClass('btn-info ');
                if (response[i] == "Perfecto") {
                    $("#button_number_" + pad(i, 2)).addClass('btn-success ');
                }
                else if (response[i] == "Defectuoso") {
                    $("#button_number_" + pad(i, 2)).addClass('btn-warning ');
                }
                else if (response[i] == "Falta") {
                    $("#button_number_" + pad(i, 2)).addClass('btn-secondary ');
                }
                else if (response[i] == "Faltan Datos") {
                    $("#button_number_" + pad(i, 2)).addClass('btn-info ');
                }

            }
            // $("#number_info").html(form_html)
            resize_buttons()
            update_colors_enabled = true;

        }).fail(function() {
            $("#hundred_container").html("Error getting existing for " + number);
            update_colors_enabled = true;
        });
    }
}

function toTitleCase(str) {
    if (str == null) {
        return str
    }
    else {
        return str.replace(/\w\S*/g, function(txt) {
              return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            }
        );
    }
}

function update_session(key, value) {
    $.post('/update_session', {
        key: key,
        value: value
    })
}

function update_session_multi(keys, values) {
    current_index = 0
    $.post('/update_session', {
        key: keys[0],
        value: values[0]
    }).done(function(response) {
        keys.shift();
        values.shift();
        if (keys.legnth > 0){
            update_session_multi(keys, values)
        }
    })
}

function set_value_or_default(key, value, title=true) {

    if (value != '' & value != null){
        aux = value
        if (title) {
            aux = toTitleCase(value)
        }
        if (typeof(aux) == "string") {
            aux = aux.replace("-l", "-L")  // For fucking Castilla-La Mancha
        }

        $("#" + key).val(aux);
    }
    else{
        $("#" + key).val("Default");
    }
}

function update_number(exp, number) {
    if (update_number_enabled & update_colors_enabled) {
        update_number_enabled = false;
        var current_number = $("#current_number").text();
        if (exp == null){
            new_number = $('#search_number').val();
            if (isNaN(new_number) | (new_number == '') | (new_number < 0) | (new_number > 99999)) {
                $('#search_number').addClass("border-danger");
                new_number = current_number;
            }
            else {
                $('#search_number').removeClass("border-danger");
            }

        }
        else {
            if (exp == 0) {
                current_number = 0
            }

            var new_number = Math.floor(current_number / Math.pow(10, exp)) * Math.pow(10, exp);
            if (exp > 2) {
                new_number = new_number + current_number % Math.pow(10, exp - 1);
            }
            new_number = new_number + number;
        }
        $("#current_number").text(pad(new_number, 5));

        var form_html =  $("#number_info").html()

        $("#number_info").html('<img class="loading" src="./static/loading.gif">');
        $.post('/get_number', {
            new_number: new_number
        }).done(function(response) {
            response = JSON.parse(response)
            $("#number_info").html(form_html);
            $("#status").val(toTitleCase(response['status']));
            set_value_or_default('origin', response['origin'])
            if (response['lot'] != null) {
                response['lot'] = response['lot'].split('/')[0];
            }
            set_value_or_default('lot', response['lot'])
            set_value_or_default('year', response['year'], title=false)
            set_value_or_default('coin', response['coin'])
            set_value_or_default('retailer_region', response['retailer_region'])
            var selection = []
            selection['province'] = toTitleCase(response['retailer_province']);
            selection['town'] = toTitleCase(response['retailer_town']);
            selection['number'] = response['retailer_number'];
            load_provinces(toTitleCase(response['retailer_region']), selection);
            update_session('retailer_region', response['retailer_region']);
            $("#retailer_town").val(toTitleCase(response['retailer_town']));
            $("#retailer_number").val(response['retailer_number']);
            $("#copies").val(response['copies']);
            update_number_enabled = true;

        }).fail(function() {
            $("#number_info").html("Error getting " + new_number);
            update_number_enabled = true;
        });

        if ((exp > 2) | (exp == null)){
            update_colors(new_number);
        }
    }
}

function load_provinces(new_region, selection = null) {
    $('select[name="retailer_region"] option[value="Default"]').prop('disabled', true);
    $.post('/update_provinces', {
        new_region: new_region
    }).done(function(response) {
        response = JSON.parse(response)
        $("#retailer_province").empty();
        $("#retailer_province").append(
            $("<option></option>")
            .attr("value", "Default")
            .text('Selecciona la provincia')
        );
        for (var i = 0; i < response.length; i++){
            $("#retailer_province").append(
                $("<option></option>")
                .attr("value", toTitleCase(response[i]))
                .text(toTitleCase(response[i]))
            );
        }
        if (selection != null) {
            $("#retailer_province").val(selection['province']);
            update_session('retailer_province', selection['province']);
            load_towns(selection['province'], selection)
        }
    }).fail(function(response) {
        console.log(response)
    });
}

function load_towns(new_province, selection = null) {
    $('select[name="retailer_province"] option[value="Default"]').prop('disabled', true);
    $.post('/update_towns', {
        new_province: new_province
    }).done(function(response) {
        response = JSON.parse(response)
        $("#retailer_town").empty();
        $("#retailer_town").append(
            $("<option></option>")
            .attr("value", "Default")
            .text('Selecciona la localidad')
        );
        for (var i = 0; i < response.length; i++){
            $("#retailer_town").append(
                $("<option></option>")
                .attr("value", toTitleCase(response[i]))
                .text(toTitleCase(response[i]))
            );
        }
        if (selection != null) {
            $("#retailer_town").val(selection['town']);
            update_session('retailer_town', selection['town']);
            $("#retailer_number").val(selection['number']);
        }
    }).fail(function(response) {
        console.log(response)
    });
}
