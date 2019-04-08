var d = new Date();
var month = d.getMonth();
const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
];
$.ajax({
  url: url_chart,
  type: "get",
  dataType: "json",
  success: function (data) {
    console.log('datos que recibo ',data);
      console.log(month,month-2);
      mes=month-2   
      if(mes == -2){
        mes = 10
      }
      if(mes == -1){
        mes = 11
      }

     
      console.log(mes)
    if(data.length != 0){
      mostrar(data);

      $('.fecha1').html('<h3>Estadísticas de las actividades <br><strong>'+monthNames[mes]+'-'+monthNames[month]+'</strong></h3>');
    }else{
      console.log('no hay datos');
      $('.fecha1').html('<h3>Estadísticas de las actividades <br><strong>'+monthNames[mes]+'-'+monthNames[month]+'</strong></h3>');
      $('#graph').append('<i class="mdi-action-info-outline large" style="color: red !important;font-size: 190px;"></i>')
      $('#graph').append('<h4>No hay estadisticas que mostrar</h4>')
    }

  },

  });
function mostrar(data){
  dict = [];
  for(var i = 0;i < data.length; i+=1){
    if(data[i].label == 'Realizadas'){
      dict.push("green");
      $('.legend').append('<span><span style="background-color:green;width: 20px;display: inline-block;margin: 5px;">&nbsp;</span>'+data[i].label+'</span>')
    }
    if(data[i].label == 'No Realizadas'){
      dict.push("red");
      $('.legend').append('<span><span style="background-color:red;width: 20px;display: inline-block;margin: 5px;">&nbsp;</span>'+data[i].label+'</span>')

    }
    if(data[i].label == 'Suspendidas'){
      dict.push("#ffc100");
      $('.legend').append('<span><span style="background-color:#ffc100;width: 20px;display: inline-block;margin: 5px;">&nbsp;</span>'+data[i].label+'</span>')

    }
}
  Morris.Donut({
    element: 'graph',
    data:data,
    labelColor: '#00B0F0',
    colors: dict,
    formatter: function (x) { return x + "%"}
  });
}

