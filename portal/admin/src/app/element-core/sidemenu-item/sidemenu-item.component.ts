import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-sidemenu-item',
  templateUrl: './sidemenu-item.component.html',
  styleUrls: ['./sidemenu-item.component.scss']
})
export class SidemenuItemComponent implements OnInit {

  @Input()
  menu;
  @Input()
  iconOnly: boolean;
  @Input()
  secondaryMenu = false;

  constructor() { }

  ngOnInit() {
  }

  openLink() {
    this.menu.open = this.menu.open;
  }
  getHeight() {
    if (this.menu.open === false) {
      return '48px';
    } else {
      if (this.menu && this.menu.sub) {
        const height = this.menu.sub.length * 56 + 56 + 'px';
        return height;
      }
    }
  }

  chechForChildMenu() {
    return this.menu && this.menu.sub ? true : false;
  }

}
