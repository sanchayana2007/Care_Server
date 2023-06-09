import { Component, OnInit, Input } from '@angular/core';
import { ObservableMedia, MediaChange } from '@angular/flex-layout';
import { SharedModule } from '../../app/shared/shared.module';
import { AUTHGWCONSTANTS } from '../../app/authorization/authconstants';
import { ToasterService } from 'angular2-toaster';
import { MatDialogConfig, MatDialog, MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { Router } from '@angular/router';
import { AuthorizationService } from './authorization.service';
import { ToolbarHelpers } from '../element-core/toolbar/toolbar.helpers';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-authorization',
  templateUrl: './authorization.component.html',
  styleUrls: ['./authorization.component.scss'],
  providers: [AuthorizationService]
})
export class AuthorizationComponent implements OnInit {

  menuElements = [
    {
      'name': 'Dashboard',
      'icon': 'dashboard',
      'link': 'dashboard'
    },
    // {
    //   'name': 'Notification',
    //   'link': 'table/notifications',
    //   'icon': 'notification_important',
    //   'open': true
    // },
    {
      'name': 'Admins',
      'link': 'table/resource/admin',
      'icon': 'account_box',
      'open': true
    },
    {
      'name': 'Users',
      'link': 'table/users',
      'icon': 'supervised_user_circle',
      'open': true
    },
    {
      'name': 'Appointments',
      'link': 'table/appointments',
      'icon': 'local_hospital',
      'open': true
    },
    {
      'name': 'Sms',
      'link': 'table/sms',
      'icon': 'sms',
      'open': true
    },
    {
      'name': 'Services',
      'link': false,
      'icon': 'add_box',
      'open': false,
      'sub': [
        {
          'name': 'Service List',
          'link': 'table/service-list',
          'icon': 'medical_services',
          'open': true
        },
        {
          'name': 'Service Providers',
          'link': 'table/service-provider',
          'icon': 'how_to_reg',
          'open': true
        },
        {
          'name': 'Products',
          'link': 'table/prodects',
          'icon': 'add_to_queue',
          'open': true
        },
      ]
    },
  ];

  @Input() isVisible = true;
  visibility = 'shown';

  sideNavOpened = true;
  matDrawerOpened = false;
  matDrawerShow = true;
  sideNavMode = 'side';
  wSocket: any;
  profileData: any;
  entityData: any;

  // tslint:disable-next-line:use-life-cycle-interface TODO:
  ngOnChanges() {
    this.visibility = this.isVisible ? 'shown' : 'hidden';
  }

  constructor(private media: ObservableMedia, private sharedModule: SharedModule,
    public dialog: MatDialog, private snackBar: MatSnackBar,
    private toasterService: ToasterService, private router: Router,
    private service: AuthorizationService) {
  }

  ngOnInit() {
    // this.initWebsocketClient();
    if (this.service.updateHeaders()) {
      this.media.subscribe((mediaChange: MediaChange) => {
        this.toggleView();
      });
      this.getEntityInfo();
      this.getAdminProfileInfo();
      this.getEntityServices();
      this.showUpProfileInfo();
    }
  }

  getEntityInfo() {
    this.service.getEntityInfo().subscribe(
      success => {
        if (success.error_code === 4003) {
          // Sign Out
          localStorage.removeItem(AUTHGWCONSTANTS.bearerToken);
          this.router.navigate(['admin/sign_in']);
          return;
        }
        if (success.resp_code) {
          const entityLogo = success.data[0].logo;
          ToolbarHelpers.currentUser.sideMenuPhotoURL = entityLogo;
        } else {
        }
      }, error => {
      });
  }
  getEntityServices() {
    this.service.getEntityServices().subscribe(
      success => {
        if (success.error_code === 4003) {
          localStorage.removeItem(AUTHGWCONSTANTS.bearerToken);
          this.router.navigate(['admin/sign_in']);
          return;
        }
        if (success.resp_code) {
          this.menuElements = success.data;
        }
      },
      error => {
      }
    );
  }

  getAdminProfileInfo() {
    this.service.getAdminProfileInfo().subscribe(success => {
      if (success.error_code === 4003) {
        // Sign Out
        localStorage.removeItem(AUTHGWCONSTANTS.bearerToken);
        this.router.navigate(['admin/sign_in']);
      } else {
        if (success.status) {
          this.profileData = success.result[0];
          this.showUpProfileInfo();
          setTimeout(() => {
          }, 400);
        }
      }
    },
      error => {
      }
    );
  }

  showUpProfileInfo() {
    // const full_name = this.profileData.firstName + ' ' +
    //   this.profileData.lastName;
    // ToolbarHelpers.currentUser.currentUserName = full_name;
    // ToolbarHelpers.currentUser.photoURL = '';

    // // ToolbarHelpers.currentUser.photoURL = this.profileData.files[0].profile;

    ToolbarHelpers.currentUser.currentUserName = 'Med Service';
  }

  initWebsocketClient(): void {
    const cntx = this;
    const ws = new WebSocket(environment.proxySocketUrl +
      '/web/rt_socket?wskey=' + localStorage.getItem(AUTHGWCONSTANTS.bearerToken) +
      '&&application_id=' + environment.applicationId);
    ws.onclose = msg => cntx.onCloseWebsocketClient();
    SharedModule.GWwebSocket = ws;
  }

  onCloseWebsocketClient(): void {
    const cntx = this;
    setTimeout(function () {
      if (
        localStorage.getItem(AUTHGWCONSTANTS.bearerToken) !== 'null' &&
        localStorage.getItem(AUTHGWCONSTANTS.bearerToken) !== null
      ) {
        cntx.initWebsocketClient();
      }
    }, 2500);
  }

  sendToSwitch(message: string): void {
    this.sharedModule.sendwsmessage(message);
    message = message.replace(/"/g, '\'');
    const msg = JSON.parse(message);
    if (msg.msg_type === 'CONN_READY') {
    } else {
      switch (msg.msg_type) {
        case 'EMERGENCY_ALERT':
          const alert_msg = 'Message: ' + msg.data[0].msg_data.title +
            '\nCustomer Name: ' + msg.data[0].user_name + '\n DriverName:' +
            msg.data[0].driver_name + '\nReg_No:' + msg.data[0].reg_num;
          this.toasterService.pop('error', 'EMERGENCY_ALERT', alert_msg);
          break;
      }
    }
  }

  sendWebSocket(): void {
    this.sharedModule.sendwsInstant(this.wSocket);
  }

  getRouteAnimation(outlet: any): any {
    return outlet.activatedRouteData.animation;
  }

  // openDialog(data): void {
  //   const dialogConfig = new MatDialogConfig();
  //   dialogConfig.autoFocus = true;
  //   dialogConfig.panelClass = ['dialog-class'];
  //   dialogConfig.height = 'auto';
  //   dialogConfig.width = '1500px';
  //   dialogConfig.data = data;
  //   const dialogConf = this.dialog.open(EmergencyDialogComponent, dialogConfig);
  //   dialogConf.afterClosed().subscribe(result => {
  //   });
  // }


  toggleView() {
    if (this.media.isActive('gt-md')) {
      this.sideNavMode = 'side';
      this.sideNavOpened = true;
      this.matDrawerOpened = false;
      this.matDrawerShow = true;
    } else if (this.media.isActive('gt-xs')) {
      this.sideNavMode = 'side';
      this.sideNavOpened = false;
      this.matDrawerOpened = true;
      this.matDrawerShow = true;
    } else if (this.media.isActive('lt-sm')) {
      this.sideNavMode = 'over';
      this.sideNavOpened = false;
      this.matDrawerOpened = false;
      this.matDrawerShow = false;
    }
  }

  openDefaultSnackBar(message: string) {
    const config = new MatSnackBarConfig();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-default'];
    config.duration = 800;
    this.snackBar.open(message, 'Close', config);
  }

  openErrorSnackBar(message: string, ) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 5000;
    this.snackBar.open(message, 'Close', config);
  }

}
