function pad(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}

function update_colors(number) {
    var button_html = $("#hundred_container").html();
    $("#hundred_container").html('<img class="loading" src="./static/loading.gif">');
    $.post('/get_existing_in_hundred', {
        number: number - (number % 100)
    }).done(function(response) {
        $("#hundred_container").html(button_html);
        response = JSON.parse(response)
        console.log(response)

        for (var i = 0; i < response.length; i++){
            $("#button_number_" + pad(i, 2)).removeClass('btn-success ').removeClass('btn-secondary ').removeClass('btn-warning ');
            if (response[i] == "Perfecto") {
                $("#button_number_" + pad(i, 2)).addClass('btn-success ');
            }
            else if (response[i] == "Defectuoso") {
                $("#button_number_" + pad(i, 2)).addClass('btn-warning ');
            }
            else if (response[i] == "Falta") {
                $("#button_number_" + pad(i, 2)).addClass('btn-secondary ');
            }

        }
        // $("#number_info").html(form_html)


    }).fail(function() {
        $("#hundred_container").html("Error getting existing for " + number);
    });
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
        // console.log($('select[name="' + key + '"] option[value="Default"]').prop('disabled'));
        // $('select[name="' + key + '"] option[value="Default"]').prop('disabled', false);
        // console.log($('select[name="' + key + '"] option[value="Default"]').prop('disabled'));
        $("#" + key).val("Default");
    }
}

function update_number(exp, number) {
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
        response['lot'] = response['lot'].split('/')[0];
        console.log(response)
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

    }).fail(function() {
        $("#number_info").html("Error getting " + new_number);
    });

    if ((exp > 2) | (exp == null)){
        update_colors(new_number);
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
