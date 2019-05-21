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
        }
    });
    });

});

//Ajax para crear el miembro
$("#modal1").on("submit", ".js-book-create-form", function (e) {
    
    var form = $(this);
    var data = $("#form :input").serializeArray();
    $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
        if (data.form_is_valid) {
            Materialize.toast('Concepto Registrado', 3000, 'rounded')
            listado_s();
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

function ver(numero){
    mostrar_modal();
    var url = window.location;

    $.ajax({
        url: url+"ver_concepto/"+numero,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
            var  form = `

            <div class="row">
                <div class="col m6 offset-m4 s12">
                <h5 class="left" style="font-size:60px;margin-top:80px;font-weight:bold;">Concepto: <br>${data.concepto}</h5>

                </div>

            </div>
            <div class="row">
                <div class="col col m6 offset-m3 s12">
              <button class="center btn btn-primary red" onclick="cerrar_modal();">Salir</button>    
                </div>
            </div>
            `;
            console.log(data);
            $("#modal1 .modal-content").html(form);

            //$("#modal1 .modal-content").append("<p>"+data.persona.cedula+"</p>");
            //$("#modal1 .modal-content").append("<p>"+data.persona.nombre+"</p>");
            
            //$("#modal1 .modal-content").append("<p>"+data.persona.apellido+"</p>");
            //$("#modal1 .modal-content").append("<p>"+data.persona.telefono+"</p>");
            //$("#modal1 .modal-content").append("<p>"+data.persona.direccion+"</p>");
            //$("#modal1 .modal-content").append("<p>"+data.persona.rol+"</p>");
            //$("#modal1 .modal-content").append("<p>"+data.persona.correo+"</p>");

        }
        });
}


function actualizar(numero){
    mostrar_modal();
    //$('#modal1 .modal-content').html(numero);

    var btn = $('.js-update');
     $(function () {
        var url = window.location;
        console.log(url);
        $.ajax({
        url: url+"actualizar/"+numero,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
            $("#modal1 .modal-content").html(data.html_form);
        }
        });
    });
}
$(document).on('click','.js-borrar',function(){
    id = this.id;
    var toastContent = '<span>¿Está seguro?</span><br><button class="btn toast-action red conf_si" id="'+id+'">Si</button>';
    Materialize.toast(toastContent, 4000);
    });

$(document).on('click','.conf_si',function(){
    $(this).attr('disabled',true)
    data = {
        id:this.id,
        csrfmiddlewaretoken:token,
    }
    $.ajax({
        url:url_delete,
        type:'POST',
        data:data,
        success:function(data){
            console.log(data.form_is_valid)
                if (data.form_is_valid) {
                    Materialize.toast('Eliminado con éxito',2000);
                    listado_s();
                }else{
                    Materialize.toast('Esta información esta siendo utilizada, no la puede eliminar.',4000);
                }
            
        },
        error:function(err){
            Materialize.toast('Error al eliminar',2000);
        }
    })
})
//Ajax para Actualizar
$("#modal1").on("submit", ".js-book-update-form", function (e) {
    
    var form = $(this);
    var data = $("#form :input").serializeArray();
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
            Materialize.toast('Concepto Actualizado', 3000, 'rounded')
            listado_s();
            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
        $("#modal1 .modal-content").html(data.html_form);
        var error = data.error.split(',');
        for(var i = 0;i < error.length; i+=1){
            $('#error').append('<p style="color:red;">'+error[i]+'</p>');
            console.log(error[i]);
        }
        }
    }
    });
    return false;


});
function listado_s(){
$.ajax({
    url : url_list,
    type:'GET',
    success:function(data){
        actualizar_data(data)

}
})
}
function actualizar_data(data){
    count = 0
    count1 = 0
    tables.clear().draw();
    for(var i = 0;i<data.length;i++){
        datos = data[i]
        var row1 = '<button onclick="actualizar('+datos.pk+')" class="btn btn-primary js-update"><i class="mdi-editor-border-color"></i></button> <a class="btn red js-borrar" id='+datos.pk+'><strong>X</strong></a>'
        var row = [count+=1,datos.fields.concepto,row1]
        tables.row.add(row).draw().node();
    }
}