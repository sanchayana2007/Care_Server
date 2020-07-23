import { Component, OnInit, Input } from '@angular/core';
import { ToolbarHelpers } from '../toolbar/toolbar.helpers';

@Component({
  selector: 'app-sidemenu',
  templateUrl: './sidemenu.component.html',
  styleUrls: ['./sidemenu.component.scss']
})
export class SidemenuComponent implements OnInit {

  @Input() iconOnly = false;
  @Input() menus = [];
  toolbarHelpers = ToolbarHelpers;

  constructor() { }

  ngOnInit() {
  }

}
