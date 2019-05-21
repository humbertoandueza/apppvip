var tables= $('#postsTable').DataTable({
    "language": {
        "url": "/static/datatables/spanish.json"
        },
    responsive: true,
    ordering: true,
    responsive: true,
    scrollY: 380,
    scrollCollapse: true,

    "iDisplayLength": 10,
    dom: 'frti<"right"p>'
    });

$(document).ready(function(){
    listado_s()
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
        $('#id_monto').addClass('number')
        }
    });
    });

});

//Ajax para crear el miembro
$("#modal1").on("submit", ".js-book-create-form", function (e) {

    var form = $(this);
    var data = $("#form :input").serializeArray();
    if($('#id_monto').val()<1){
        $('#error').html('<p style="color:red; margin-left:40px;">Introduzca un valor valido</p>');
        $( "#id_monto" ).addClass( "invalid" );

        return false;
    }
    if(moment($('#id_fecha').val()) >moment()){
        $('#error').html('<p style="color:red; margin-left:40px;">Fecha invalida: Introduzca una fecha igual o menor a la actual.</p>');
        $( "#id_fecha" ).addClass( "invalid" );

        return false;
    }
    for (var i = 0; i < data.length; i+=1) {
        if(data[i].name == "cedula"){
            //console.log('cedula: ', data[i].value.length);
            if(data[i].value.length <=6 || data[i].value.length >8 ){
                $( "#id_cedula" ).addClass( "invalid" );
                $('#error').html('<p style="color:red; margin-left:40px;">La cedula no es correcta</p>');
                //alert('La cedula no cumple con lo requerido');
                return false;
            }
        }
    }

    $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
        if (data.form_is_valid) {
            Materialize.toast('Ingreso Registrado', 3000, 'rounded')
            capital();
            listado_s()
            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
            $("#modal1 .modal-content").html(data.html_form);
            var error = data.error.split(',');
            for(var i = 0;i < error.length; i+=1){
                $('#error').append('<p style="color:red;">'+error[i]+'</p>');
                
            }

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
        url: url+"/actualizar/"+numero,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
            $("#modal1 .modal-content").html(data.html_form);
            $('#id_monto').addClass('number')


        }
        });
    });
}
//Ajax para Actualizar
$("#modal1").on("submit", ".js-book-update-form", function (e) {

    var form = $(this);
    var data = $("#form :input").serializeArray();
    if($('#id_monto').val()<1){
        $('#error').html('<p style="color:red; margin-left:40px;">Introduzca un valor valido</p>');
        $( "#id_monto" ).addClass( "invalid" );

        return false;
    }
    if(moment($('#id_fecha').val()) >moment()){
        $('#error').html('<p style="color:red; margin-left:40px;">Fecha invalida: Introduzca una fecha igual o menor a la actual.</p>');
        $( "#id_fecha" ).addClass( "invalid" );

        return false;
    }

    $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
        if (data.form_is_valid) {
            Materialize.toast('Ingreso Actualizado', 3000, 'rounded')
            capital();
            listado_s()
            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
            $("#modal1 .modal-content").html(data.html_form);
            $("#error").html("<p style='color:red;' class='center'>"+data.error+"</p>");
            console.log(data.error);

        }
    }
    });
    return false;
});
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
function mostrar_modal(){
    $('#modal1 .modal-content').html(loader);
    $('.modal-full').css("display", "block");
    $('.modal-full').css("z-index", "1003");
}

//modals personalizados
function cerrar_modal(){
    $('.modal-full').css("display", "none");
    $('#modal1 .modal-content').html(loader);
}
function listado_s(){
    $.ajax({
        url : url_list,
        type:'GET',
        success:function(data){
            if (data.length>0) {
                actualizar_data(data)
                $('.impr').css('display','block');
            }else{
                $('.impr').css('display','none');
            }


    }
    })
}
function actualizar_data(data){
    count = 0
    count1 = 0
    tables.clear().draw();
    for(var i = 0;i<data.length;i++){
        datos = data[i]
        var row1 = '<button onclick="actualizar('+datos.pk+')" class="btn btn-primary js-update center"><i class="mdi-editor-border-color"></i></button>'
        var row = [count+=1,datos.fields.fecha,datos.fields.monto,datos.fields.cedula,datos.fields.persona,datos.fields.tipo_de_pago,row1]
        tables.row.add(row).draw().node();
    }
}