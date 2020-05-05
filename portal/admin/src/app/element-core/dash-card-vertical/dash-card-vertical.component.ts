import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-dash-card-vertical',
  templateUrl: './dash-card-vertical.component.html',
  styleUrls: ['./dash-card-vertical.component.scss']
})
export class DashCardVerticalComponent implements OnInit {


  @Input() dashData: any;

  constructor() {

  }

  ngOnInit() {
  }

}
