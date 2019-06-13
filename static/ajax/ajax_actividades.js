$(document).ready(function(){
    $('select').material_select();
    });

    //ajax para obtener el formulario
 $(function () {

    $(".modal-full-screen").click(function () {
        mostrar_modal();
    $.ajax({
        url: url_crear,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
        $("#modal1 .modal-content").html(data.html_form);
        $('#close').addClass('hidden');
        }
    });
    });

});

//Ajax para crear el miembro
$("#modal2").on("submit", ".js-book-create-form", function (e) {
    var form = $(this);
    var datos = $("#form :input").serializeArray();
    id_nombre = $('#id_nombre').val()
    id_descripcion = $('#id_descripcion').val()
    id_lugar = $('#id_lugar').val()
    id_persona = $('#id_persona').val()
    id_tipo = $('#id_tipo').val()
    id_fecha = $('#id_fecha').val()
    id_fecha1 = $('#id_fecha1').val()
    id_hora = $('#id_hora').val()
    if( $('#entrenamiento').length){
        entrenamiento = $('#entrenamiento').val()
    }else{
        entrenamiento = ''
    }
    token = $("input[name=csrfmiddlewaretoken]").val();
    dias = $('#dias')
    data1 = []

    if (dias.length){
        if($('#dias').val()>0 && $('#dias').val()<6 && id_tipo == 3){
            count = 0
            for(var i =0;i<$('#dias').val();i++){
                fec = id_fecha1.split('/')
                fec1 = fec[2]+'-'+fec[1]+'-'+fec[0]
                fecha = moment(fec1).add(count,'days').format('YYYY-MM-DD')
                count += 7
                dia1 = moment(fecha).day()

                is_domingo = false;
                
                if($('#dias').val() >1){
                    parte = ' (Parte '+(i+1)+')'
                }else{
                    parte = ''
                }
                arr = {
                    "nombre" :id_nombre +parte,
                    "descripcion":id_descripcion,
                    "lugar":id_lugar,
                    "persona":id_persona,
                    "tipo":id_tipo,
                    "fecha":fecha,
                    "hora":id_hora,
                    "is_domingo":is_domingo,
                    "entre":entrenamiento
                }
                data1.push(arr)
            }
        }if($('#dias').val()>5){
            $('#error').html('<p style="color:red;text-aling:center;">Cantidad  de dias:Introduzca un numero menor a 5</p>')
            $('#dias').focus()
        }if($('#dias').val()<1){
            $('#error').html('<p style="color:red;text-aling:center;">Cantidad  de dias:Introduzca un numero mayor a 0</p>')
            $('#dias').focus()

        }
        if($('#dias').val()>0 && $('#dias').val()<6 && (id_tipo == 1 || id_tipo == 2)){
            count = 0
            for(var i =0;i<$('#dias').val();i++){
                if($('#dias').val() >1){
                    dia = ' (Día '+(i+1)+')'
                }else{
                    dia = ''
                }
                fec = id_fecha.split('/')
                fec1 = fec[2]+'-'+fec[1]+'-'+fec[0]
                fecha = moment(fec1).add(count,'days').format('YYYY-MM-DD')
                dia1 = moment(fecha).day()
                if(dia1 == 0){
                    is_domingo= true;
                }else{
                    is_domingo = false;
                }
                count += 1
                arr = {
                    "nombre" :id_nombre +dia,
                    "descripcion":id_descripcion,
                    "lugar":id_lugar,
                    "persona":id_persona,
                    "tipo":id_tipo,
                    "fecha":fecha,
                    "hora":id_hora,
                    "is_domingo":is_domingo,
                    "entre":entrenamiento
                }
                data1.push(arr)
            }
        }
    }
    else{
        fec = id_fecha.split('/')
        fec1 = fec[2]+'-'+fec[1]+'-'+fec[0]
        fecha = moment(fec1).format('YYYY-MM-DD')
        dia1 = moment(fecha).day()
        if(dia1 == 0){
            is_domingo= true;
        }else{
            is_domingo = false;
        }
        arr = {
            "nombre" :id_nombre,
            "descripcion":id_descripcion,
            "lugar":id_lugar,
            "persona":id_persona,
            "tipo":id_tipo,
            "fecha":fecha,
            "hora":id_hora,
            "is_domingo":is_domingo,
            "entre":entrenamiento
        }
        data1.push(arr)
    } 
    data = {
        data : JSON.stringify(data1),
        csrfmiddlewaretoken:token,
    }
    $.ajax({
    url: form.attr("action"),
    data: data,
    type: 'POST',
    success: function (data) {
        console.log(data)
        
        if (data.form_is_valid) {
            Materialize.toast('Actividad Registrada', 3000, 'rounded')
            for(var i =0;i<data.data.length;i++){
                $('#calendar').fullCalendar('renderEvent', {
                    id: data.data[i].id,
                    title: data.data[i].title,
                    start: data.data[i].start,
                    descripcion:data.data[i].descripcion,
                    lugar:data.data[i].lugar,
                    tipo:data.data[i].tipo,
                    observacion:data.data[i].observacion,
                    estatus:'Por Realizar',
                    estatuss:data.data[i].estatuss,
                    color : '#00B0F0',
                    allDay: false
                  });

            }
            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
            $("#modal2 .modal-content").html(data.html_form);
            var error = data.error;
            $('#error').html('<p style="color:red;text-align:center;">'+error+'</p>');

        }
    }
    });
    return false;
});

//Ajax para obtener form Actualizar
function actualizar(numero){
    mostrar_modal();
    //$('#modal1 .modal-content').html(numero);

    var btn = $('.js-update');
     $(function () {
        var url = window.location;
        $.ajax({
        url: url+"actualizar/"+numero,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
            $("#modal2 .modal-content").html(data.html_form);
        }
        });
    });
}
//Ajax para Actualizar
$("#modal2").on("submit", ".js-book-update-form", function (e) {
    e.preventDefault()
    var form = $(this);
    obs = $('#id_observacion').val()
    if(obs){
        if($('#id_observacion').val().length >500){
            $('#error').html('<p style="color: red;">El campo supera la cantidad permitida de caracteres.</p>')
            $('#id_observacion').addClass('invalid')
            return false;
        }
    }
    $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
        console.log('editando',data)
        if (data.form_is_valid) {
            Materialize.toast('Estatus Actualizado', 3000, 'rounded');
            if(data.create){
                $('#calendar').fullCalendar('renderEvent', {
                    id: data.id,
                    title: data.title,
                    start: data.start,
                    descripcion:data.descripcion,
                    lugar:data.lugar,
                    tipo:data.tipo,
                    observacion:data.observacion,
                    estatus:data.estatus,
                    estatuss:data.estatuss,
                    color : data.color,
                    allDay: false
                  });
            }else{
                evento.color = data.color,
                evento.estatus = data.estatus,
                evento.estatuss = data.estatuss,
                evento.start = data.start,
                evento.observacion=data.observacion,
                evento.tipo=data.tipo,

                $('#calendar').fullCalendar('updateEvent', evento);
            }

            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
        $("#modal2 .modal-content").html(data.html_form);
        }
    }
    });
    return false;
});

$("#modal2").on("submit", ".js-book-edit-form", function (e) {
    e.preventDefault()
    var form = $(this);
    $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
        console.log(data)
        if (data.form_is_valid) {
            Materialize.toast('Actividad Actualizada', 3000, 'rounded');
                evento.title = data.title,
                evento.descripcion = data.descripcion,
                evento.lugar = data.lugar,
                evento.color = data.color,
                evento.estatus = data.estatus,
                evento.estatuss = data.estatuss,
                evento.observacion=data.observacion,
                evento.tipo=data.tipo,
                evento.start = data.start,

                $('#calendar').fullCalendar('updateEvent', evento);
            

            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
        $("#modal2 .modal-content").html(data.html_form);
        }
    }
    });
    return false;
});

//Ajax para obtener los datos a Borrar
function borrar(numero){
    mostrar_modal();
    //$('#modal1 .modal-content').html(numero);

    var btn = $('.js-borrar');
     $(function () {
        var url = window.location;
        $.ajax({
        url: url+"borrar/"+numero,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
            $("#modal2 .modal-content").html(data.html_form);
        }
        });
    });
}

//Ajax para borrar
$("#modal2").on("submit", ".js-book-borrar-form", function (e) {
            
    var form = $(this);
    $.ajax({
    url: form.attr("action"),
    type: 'get',
    dataType: 'json',
    success: function (data) {
        if (data.form_is_valid) {
            Materialize.toast('Miembro Eliminado', 3000, 'rounded')
            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
        $("#modal2 .modal-content").html(data.html_form);
        }
    }
    });
    return false;
});
$(document).on('change','#id_tipo',function(){
    this.value
    metodo = $('#form1');
    console.log(metodo)
    if(metodo != 'js-book-edit-form'){
        if(!$('#form1').hasClass('js-book-edit-form')){
            if(this.value == 3 || this.value == 2 || this.value == 1){
                html = `<div class="input-field col s12 m12">
                            <input type="number" name="nombre" class="validate number" id="dias" required="">
                            <label for="dias" class="active">Cantidad de dias</label>
                        </div>`
                $('#num').html(html)
                if(this.value == 3){
                    $('#id_hora').val('09:00:00')
                    $('#id_hora').attr('readonly','readonly')
                    $('#id_fecha').addClass('hide')
                    $('#id_fecha1').removeClass('hide')
                    $('#id_fecha1').removeAttr('disabled')
                    $('#id_fecha1').attr('required','required')
                    $('#id_fecha').removeAttr('required')
                    $('#id_fecha').attr('disabled','disabled')

                }else{
                    $('#id_hora').val('')

                    $('#id_hora').removeAttr('readonly')

                    $('#id_fecha').removeClass('hide')
                    $('#id_fecha').attr('required','required')
                    $('#id_fecha1').addClass('hide')
                    $('#id_fecha').removeAttr('disabled')

                    $('#id_fecha1').removeAttr('required')

                    $('#id_fecha1').attr('disabled','disabled')
                }



            }else{
                $('#id_hora').val('')

                $('#id_hora').removeAttr('readonly')

                $('#id_fecha').removeClass('hide')
                $('#id_fecha1').addClass('hide')
                $('#id_fecha').removeAttr('disabled')

                $('#id_fecha').attr('required','required')

                $('#id_fecha1').removeAttr('required')

                $('#id_fecha1').attr('disabled','disabled')
                $('#num').html('')
            }
            
        }

    }
    
})
var loader = `
<div class="preloader-wrapper active" style="margin-top:5%;">
    <div class="spinner-layer spinner-blue-only">
        <div class="circle-clipper left">
        <div class="circle"></div>
        </div>
        <div class="gap-patch">
        <div class="circle"></div>
        </div>
        <div class="circle-clipper right">
        <div class="circle"></div>
        </div>
    </div>
</div>
`;
var pre = `
<div class="row">
<div class="col s6 offset-s3 m6 offset-m3">
<div class="progress">
      <div class="indeterminate"></div>
</div>
</div>
</div>`;
pdf = ''

function mostrar_modal(){
    $('#modal2 .modal-content').html(loader);
    $('.modal-full').css("display", "block");
    $('.modal-full').css("z-index", "1003");
}

//modals personalizados
function cerrar_modal(){
    $('#cargar').css("display","none");
    $('#gallery').css("display","none");
    $("#gallery").html("");
    $("#pdf").html("");


    $('#cerrar').css("display","none");
    $('.modal-full').css("display", "none");
    $('#modal2 .modal-content').html(loader);
}