import { Component, OnInit, HostListener, Input, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import { AUTHGWCONSTANTS } from '../../authorization/authconstants';
import { ToolbarHelpers } from './../toolbar/toolbar.helpers';
import { SharedModule } from 'src/app/shared/shared.module';
import { ProfileComponent } from './../../components/profile/profile.component';
// import {AuthConstants} from '../../authorization/authconstants';
import {ElementCoreService} from './../element-core.service';
import {HelpComponent} from './../../components/help/help.component';
import {MatDialogConfig, MatSnackBarConfig, MatSnackBar, MatDialog} from '@angular/material';
@Component({
  selector: 'app-user-menu',
  templateUrl: './user-menu.component.html',
  styleUrls: ['./user-menu.component.scss'],
  providers: [ElementCoreService]
})
export class UserMenuComponent implements OnInit {

  isOpen = false;
  profileData: any;
  // currentUser = null;
  uName = 'Soumik Debnath';

  @Input() currentUser = null;
  @HostListener('document:click', ['$event', '$event.target'])
  onClick(event: MouseEvent, targetElement: HTMLElement) {
    if (!targetElement) {
      return;
    }

    const clickedInside = this.elementRef.nativeElement.contains(targetElement);
    if (!clickedInside) {
      this.isOpen = false;
    }
  }

  constructor(private elementRef: ElementRef, private router: Router, public dialog: MatDialog,
    private snackBar: MatSnackBar, private service: ElementCoreService) { }

  ngOnInit() {
    this.getAdminInfo();
  }
  getAdminInfo() {
    this.service.getAdminInfo().subscribe(
      success => {
        if (success.error_code === 3) {
          // Sign Out
          localStorage.removeItem(AUTHGWCONSTANTS.bearerToken);
          localStorage.removeItem(AUTHGWCONSTANTS.xOriginKey);
          localStorage.removeItem(AUTHGWCONSTANTS.xApiKey);
          this.router.navigate(['sign_in']);
        } else {
          if (success.resp_code) {
            this.profileData = success.data[0];
            // this.showUpProfileInfo();
          }
        }
      },
      error => {
      }
    );
  }

  // showUpProfileInfo() {
  //   ToolbarHelpers.currentUser.currentUserName = this.profileData.full_name;
  //   ToolbarHelpers.currentUser.photoURL = this.profileData.profile_info[0].profile_pic;
  // }
  OnHelp() {
    // const data = { dialog_data: this.profileData };
    // this.openHelpDialog(data);
  }
  onCreate() {
    // const data = { dialog_data: this.profileData };
    // this.openDialog(data);
  }
  onRefresh() {
    this.openSnackBar('Refreshing ....');
  }
  sign_out() {
    localStorage.removeItem(AUTHGWCONSTANTS.bearerToken);
    this.router.navigate(['sign_in']);
    if (SharedModule.GWwebSocket !== null) {
      SharedModule.GWwebSocket.close();
      SharedModule.GWwebSocket = null;
    }
  }
  openDialog(data): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.panelClass = ['dialog-class'];
    dialogConfig.height = 'auto';
    dialogConfig.width = '900px';
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(ProfileComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(result => {
      if (ElementCoreService.dialogResult) {
        this.onRefresh();
      } else {
      }
    });
  }
  openHelpDialog(data): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.panelClass = ['dialog-class'];
    dialogConfig.height = 'auto';
    dialogConfig.width = '500px';
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(HelpComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(result => {
      if (ElementCoreService.dialogResult) {
        this.onRefresh();
      } else {
      }
    });
  }

  openSnackBar(message: string) {
    const config = new MatSnackBarConfig();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class'];
    config.duration = 500;
    this.snackBar.open(message, 'Close', config);
  }

}
