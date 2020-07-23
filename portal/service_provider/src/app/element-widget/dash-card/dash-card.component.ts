import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dash-card',
  templateUrl: './dash-card.component.html',
  styleUrls: ['./dash-card.component.scss']
})
export class DashCardComponent implements OnInit {

  @Input() data: any;
  @Input() iconOnly: boolean;

  constructor(private router: Router) {

  }

  ngOnInit() {
  }

  onClick(): void {
    if (this.data) {
      this.router.navigateByUrl(this.data.routerLink);
    } else {
      this.router.navigateByUrl(null);
    }
  }

}
