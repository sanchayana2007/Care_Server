
import * as am4core from '@amcharts/amcharts4/core';
import * as am4charts from '@amcharts/amcharts4/charts';
import am4themes_animated from '@amcharts/amcharts4/themes/animated';
am4core.useTheme(am4themes_animated);

export class AppChartHandler {

    public static createBasicLineChartFromAmChart(elementId: string,
        fillOpacity: number, strokeWidth: number, zoomA: number,
        zoomB: number, bulletSize: number): any {

        // Create Chart
        const chart: any = am4core.create(elementId, am4charts.XYChart);
        chart.data = [];
        const dateAxis = chart.xAxes.push(new am4charts.DateAxis());
        chart.yAxes.push(new am4charts.ValueAxis());

        // Create series
        const series = chart.series.push(new am4charts.LineSeries());
        series.dataFields.valueY = 'value';
        series.dataFields.dateX = 'date';
        series.tooltipText = '{value}';
        series.minBulletDistance = 15;
        series.fillOpacity = fillOpacity;
        series.strokeWidth = strokeWidth;

        // Drop-shaped tooltips
        series.tooltip.background.cornerRadius = 0;
        series.tooltip.background.strokeOpacity = 0;
        series.tooltip.pointerOrientation = 'vertical';
        series.tooltip.label.minWidth = 40;
        series.tooltip.label.minHeight = 40;
        series.tooltip.label.textAlign = 'middle';
        series.tooltip.label.textValign = 'middle';

        // Make bullets grow on hover
        const bullet = series.bullets.push(new am4charts.CircleBullet());
        bullet.circle.strokeWidth = 2;
        bullet.circle.radius = bulletSize;
        bullet.circle.fill = am4core.color('#fff');

        const bullethover = bullet.states.create('hover');
        bullethover.properties.scale = 1.3;

        // Make a panning cursor
        chart.cursor = new am4charts.XYCursor();
        chart.cursor.behavior = 'panXY';
        // chart.cursor.xAxis = valueAxis;
        chart.cursor.snapToSeries = series;

        // Create vertical scrollbar and place it before the value axis
        chart.scrollbarY = new am4core.Scrollbar();
        chart.scrollbarY.parent = chart.leftAxesContainer;
        chart.scrollbarY.toBack();

        // Create a horizontal scrollbar with previe and place it underneath the date axis
        chart.scrollbarX = new am4charts.XYChartScrollbar();
        chart.scrollbarX.series.push(series);
        chart.scrollbarX.parent = chart.bottomAxesContainer;

        chart.events.on('ready', function () {
            dateAxis.zoom(
                {
                    start: zoomA,
                    end: zoomB
                }
            );
        });
        return chart;
    }

    public static createBasicPieChartFromAmChart(elementId: string): any {
        const chart = am4core.create(elementId, am4charts.PieChart);
        // Add and configure Series
        const pieSeries = chart.series.push(new am4charts.PieSeries());
        pieSeries.dataFields.value = 'litres';
        pieSeries.dataFields.category = 'country';
        pieSeries.slices.template.stroke = am4core.color('#fff');
        pieSeries.slices.template.strokeWidth = 2;
        pieSeries.slices.template.strokeOpacity = 1;

        // This creates initial animation
        pieSeries.hiddenState.properties.opacity = 1;
        pieSeries.hiddenState.properties.endAngle = -90;
        pieSeries.hiddenState.properties.startAngle = -90;
        return chart;
    }

    public static create3DPieChartFromAmChart(elementId: string): any {
        const chart = am4core.create(elementId, am4charts.PieChart3D);
        const series = chart.series.push(new am4charts.PieSeries3D());
        series.dataFields.value = 'value';
        series.alignLabels = false,
        series.colors.step = 3;
        series.dataFields.category = 'country';
        chart.legend = new am4charts.Legend();
        return chart;
    }

}
