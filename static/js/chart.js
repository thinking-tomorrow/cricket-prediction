function convert_to_list(data){
  teams=data['data']; 
  team_list=[]
  val_list=[]
  for (team in teams){
    team_list.push(team);
    val_list.push(teams[team]);
  }

  return [team_list, val_list]
}

function plot_chart(id, type, title, x, y, y_title){
  var myChart = Highcharts.chart(id, {
    chart: {
      type: type
    },
    title: {
      text: title
    },
    xAxis: {
      categories: x
    },
    yAxis: {
      title: {
        text: y_title
      }
    },
    series: [{
      data: y
    }]
  });
}

$(document).ready(function(){
    
  url='api/match_winners';
  $.get(url, function(data){
    teams_list=convert_to_list(data);
    plot_chart('container', 'column', 'Matches Won By Each Team Over the Years', teams_list[0], teams_list[1], 'Matches Won')
  });

  url='api/max_moms'
  $.get(url, function(data){
    moms_list=convert_to_list(data);
    plot_chart('container2', 'column', 'Maximum Man of the Match Awards Won', moms_list[0], moms_list[1], 'Awards Won')
  });

  url='api/max_moms'
  $.get(url, function(data){
    moms_list=convert_to_list(data);
    plot_chart('container2', 'column', 'Maximum Man of the Match Awards Won', moms_list[0], moms_list[1], 'Awards Won')
  });

  $('.season_checkbox').change(function(){
    checked=$(this).is(':checked');
    $('.season_select').toggle();
    
    if(checked==true){

    }
    else{

    }
  });

  $('.season_select').change(function(){
    season=$(this).val();
    data_chart=$(this).parent().parent().attr('data-chart-name');
    data_url=$(this).parent().parent().attr('data-url');
    data_title=$(this).parent().parent().attr('data-title');
    data_title_y=$(this).parent().parent().attr('data-title-y');

    url='api/season_'+data_url+'/'+season

    $.get(url, function(data){
      data_list=convert_to_list(data);
      plot_chart(data_chart, 'column', data_title, data_list[0], data_list[1], data_title_y);
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  url='api/toss_details'

  $.get(url, function(data){
    toss_data=convert_to_list(data);
    console.log(toss_data)

    labels = toss_data[0];
    values = toss_data[1];

    toss_win = values[1]
    toss_loss = values[0]
    label_1 = labels[0]
    label_2 = labels[1]

    var myChart = Highcharts.chart('pie', {
      chart: {
          type: 'pie'
      },
      title: {
          text: 'Fruit Consumption'
      },
      xAxis: {
          
      },
      yAxis: {
          title: {
              text: 'Fruit eaten'
          }
      },
      series: [{
        data: [{
        name: label_1,
        y: toss_win,
        sliced: true,
        selected: true
      },{
        name: label_2,
        y: toss_loss        
      }]
      }]
    });
  });
});
