import { Component, OnInit, Input } from '@angular/core';
import { AppChartHandler } from 'src/app/handler/AppChartHandler';

@Component({
  selector: 'app-graph-card',
  templateUrl: './graph-card.component.html',
  styleUrls: ['./graph-card.component.scss']
})
export class GraphCardComponent implements OnInit {

  @Input() data: any;
  @Input() index: number;
  msg: string;

  constructor() {

  }

  ngOnInit() {
    this.msg = this.data.title;
    const chartId = 'statusChart' + this.index;
    document.getElementById('statusChart').id = chartId;
    const chart = AppChartHandler.create3DPieChartFromAmChart(chartId);
    chart.data = this.data.data;
  }

}
