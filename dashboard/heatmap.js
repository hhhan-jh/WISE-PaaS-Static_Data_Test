// [1] 데이터 구조에 맞게 '진짜 데이터' 꺼내기
var seriesList = [];

// 로그를 보니 data.series 안에 배열이 들어있습니다.
if (data && data.series) {
    seriesList = data.series;
} else if (Array.isArray(data)) {
    // 혹시라도 data가 바로 배열인 경우를 대비
    seriesList = data;
}

// [2] X, Y 데이터 찾기
var xSeries = null;
var ySeries = null;

if (seriesList && seriesList.length) {
    for (var i = 0; i < seriesList.length; i++) {
        if (seriesList[i].target === 'x') {
            xSeries = seriesList[i];
        } else if (seriesList[i].target === 'y') {
            ySeries = seriesList[i];
        }
    }
}

// [3] 좌표 합치기
var points = [];

if (xSeries && ySeries && xSeries.datapoints && ySeries.datapoints) {
    // 데이터 개수 중 적은 쪽에 맞춤
    var len = Math.min(xSeries.datapoints.length, ySeries.datapoints.length);

    for (var j = 0; j < len; j++) {
        // datapoints 구조: [값, 시간] -> [0]번째가 값
        var xVal = xSeries.datapoints[j][0];
        var yVal = ySeries.datapoints[j][0];
        
        // 값이 숫자인지 확인하고 추가
        if (typeof xVal === 'number' && typeof yVal === 'number') {
            points.push([xVal, yVal]);
        }
    }
}

// [4] 차트 옵션 설정
return {
  backgroundColor: '#1f1d1d', 
  title: {
    text: '위험 구역 분포도 (Data: ' + points.length + '건)',
    left: 'center',
    textStyle: { color: '#eee' }
  },
  tooltip: {
    trigger: 'item',
    formatter: function (params) {
       if (Array.isArray(params.data)) {
          return '위치: (' + params.data[0].toFixed(2) + ', ' + params.data[1].toFixed(2) + ')';
       }
       return '';
    }
  },
  grid: {
    left: '10%', right: '10%', bottom: '15%', top: '20%'
  },
  xAxis: {
    name: 'X (Meter)',
    type: 'value',
    min: -5, max: 5, 
    splitLine: { show: true, lineStyle: { type: 'dashed', color: '#333' } },
    axisLabel: { color: '#ccc' },
    axisLine: { lineStyle: { color: '#ccc' } }
  },
  yAxis: {
    name: 'Y (Meter)',
    type: 'value',
    min: -5, max: 5,
    splitLine: { show: true, lineStyle: { type: 'dashed', color: '#333' } },
    axisLabel: { color: '#ccc' },
    axisLine: { lineStyle: { color: '#ccc' } }
  },
  series: [{
    name: 'Danger Points',
    type: 'scatter', 
    symbolSize: 15, 
    data: points, 
    
    itemStyle: {
        // 빨간색(255,0,0) + 투명도 0.1 -> 겹치면 진해짐
        normal: {
            color: 'rgba(255, 0, 0, 0.1)', 
            borderColor: 'rgba(255, 0, 0, 0.2)',
            borderWidth: 1
        }
    }
  }]
};