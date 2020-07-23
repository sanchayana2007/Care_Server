import { Component, OnInit, Input } from '@angular/core';
import { DashBoardElements } from './dashboard-elements';
import * as screenfull from 'screenfull';
import { DashboardService } from './dashboard.service';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  providers: [DashboardService],
})
export class DashboardComponent implements OnInit {

  data: any;
  googleMap: any;

  public dashCardFour = DashBoardElements.dashCardsFour;
  public graphCard = DashBoardElements.graphCards;
  public dashCardTotal = DashBoardElements.dashCardsTotal;
  public dashCardRunning = DashBoardElements.dashCardsRunning;
  public dashCardIdle = DashBoardElements.dashCardsIdle;
  public dashCardInactive = DashBoardElements.dashCardsInactive;
  public dashCardStop = DashBoardElements.dashCardsStop;
  public dashCardNoData = DashBoardElements.dashCardsNoData;
  isScreen = false;
  // elem: any;

  constructor(private service: DashboardService) {
    // ToolbarHelpers.toolbarTitle = 'Dashboard';
   }

  ngOnInit() {
    this.getDashBoardReport();
  }

  // openFullscreen() {
  //   this.elem = document.getElementById('myvideo');
  //   if (this.elem.requestFullscreen) {
  //     this.elem.requestFullscreen();
  //   } else if (this.elem.mozRequestFullScreen) {
  //     this.elem.mozRequestFullScreen();
  //   } else if (this.elem.webkitRequestFullscreen) {
  //     this.elem.webkitRequestFullscreen();
  //   } else if (this.elem.msRequestFullscreen) {
  //     this.elem.msRequestFullscreen();
  //   }
  // }

  dashTotall() {
  }

  dashRunning() {
  }

  dashIdle() {
  }

  dashInactive() {
  }

  dashStop() {
  }
  dashNoData() {
  }

  getDashBoardReport() {
    this.service.getDashBoardReport().subscribe(
      success => {
        if (success.status) {
          this.loadReportData(success.result);
        } else {

        }
      },
      error => {
      }
    );
  }

  loadReportData(data: any) {
    console.log("DATAAAAAAAAAA",data);
    if (data !== undefined && data !== null
      && data.length !== 0) {
      for (let i = 0; i < data.length; i++) {
        if (data[i].touristCount !== undefined || data[i].touristCount !== null ||
          data[i].touristCount !== '') {
          this.dashCardFour[0].number = data[i].touristCount;
        } else {
          this.dashCardFour[0].number = 0;
        }
        if (data[i].accomdationCount !== undefined || data[i].accomdationCount !== null ||
          data[i].accomdationCount !== '') {
          this.dashCardFour[1].number = data[i].accomdationCount;
        } else {
          this.dashCardFour[1].number = 0;
        }
        // if (data[i].total_vehicles !== undefined || data[i].total_vehicles !== null ||
        //   data[i].total_vehicles !== '') {
        //   this.dashCardFour[2].number = data[i].total_vehicles;
        // } else {
        //   data[i].total_vehicles_text = 'N/A';
        // }
        // if (data[i].total_devices !== undefined || data[i].total_devices !== null ||
        //   data[i].total_devices !== '') {
        //   this.dashCardFour[3].number = data[i].total_devices;
        // } else {
        //   data[i].total_devices_text = 'N/A';
        // }
      }
    }
  }

  toggleFullScreen() {
    const elem = document.getElementById('full_screen');
    if (this.isScreen) {
      screenfull.toggle();
      this.isScreen = !this.isScreen;
      return;
    }
    if (screenfull.enabled) {
      screenfull.request(elem);
    } else {
      screenfull.toggle();
    }
    this.isScreen = !this.isScreen;
  }
}
