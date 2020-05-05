import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { AUTHGWCONSTANTS } from '../../../../authorization/authconstants';
import { AdminService } from '../admin.service';

@Component({
  selector: 'app-admin-dialog',
  templateUrl: './admin-dialog.component.html',
  styleUrls: ['./admin-dialog.component.scss'],
  providers: [AdminService]
})
export class AdminDialogComponent implements OnInit {
  title: string;
  data: any;
  root = true;
  password = false;
  disabledStatus = false;
  loadAdmin = false;
  dialogState = 0;
  componentClosed = false;
  componentClosedValue = 0;
  componentClosedTitle = '';

  constructor(public thisDialogRef: MatDialogRef<AdminDialogComponent>,
    @Inject(MAT_DIALOG_DATA) private dailogData: any, private service: AdminService,
    private snackBar: MatSnackBar) {
    this.dailogData = JSON.stringify(this.dailogData);
    this.dailogData = JSON.parse(this.dailogData);
    this.data = this.dailogData.dialog_data;

    if (!localStorage.getItem(AUTHGWCONSTANTS.bearerToken) ||
      !localStorage.getItem(AUTHGWCONSTANTS.xApiKey) ||
      !localStorage.getItem(AUTHGWCONSTANTS.xOriginKey)) {
      this.root = true;
    } else {
      this.root = false;
      this.password = true;
    }
    if (this.data) {
      this.dialogState = 2;
      this.disabledStatus = true;
      this.title = 'Edit Admin Detials';
      const f_name_text = this.data.full_name_text.split(' ');
      this.data.first_name_text = f_name_text[0];
      if (f_name_text.length > 0) {
        for (let i = 1; i < f_name_text.length; i++) {
          this.data.last_name_text = '';
          this.data.last_name_text += f_name_text[i];
        }
      }
      this.data.contact_number_text = this.data.contact_number_text;
      this.data.email_text = this.data.email_text;
      this.password = true;
      this.root = true;
      this.data.password = 0;
    } else {
      this.dialogState = 1;
      this.title = 'Add Admin Detials';
      this.data = {};
      this.data.closed = false;
      this.data.first_name_text = '';
      this.data.last_name_text = '';
      this.data.contact_number_text = null;
      this.data.email_text = '';
      this.data.password = '';
      this.password = false;
    }
    if (this.data.closed) {
      this.componentClosed = true;
      this.componentClosedTitle = 'Disabled';
    } else {
      this.componentClosedTitle = 'Enabled';
    }
  }

  ngOnInit() {

  }

  onChange(event) {
    if (event.checked === false) {
      this.data.Closed = false;
      this.componentClosedTitle = 'Enabled';
      this.componentClosedValue = 0;
    } else if (event.checked === true) {
      this.data.Closed = true;
      this.componentClosedTitle = 'Disabled';
      this.componentClosedValue = 1;
    }
  }

  onClose(): void {
    AdminService.dialogResult = false;
    this.thisDialogRef.close();
  }

  onSave() {
    if (this.isValid()) {
      this.loadAdmin = true;
      if (this.dialogState === 2) {
        // edit admin
        const body = {
          id: this.data.id,
          closed: this.data.closed,
          firstName: this.data.first_name_text,
          lastName: this.data.last_name_text,
          countryCode: 91,
          phoneNumber: this.data.contact_number_text,
          email: this.data.email_text
        };
        this.service.editAdmins(body).subscribe(success => {
          if (success.status) {
            AdminService.dialogResult = true;
            this.thisDialogRef.close();
            this.openSuccessSnackBar(success.message);
          } else {
            AdminService.dialogResult = false;
            this.openErrorSnackBar(success.message);
          }
          this.loadAdmin = false;
        }, error => {
          AdminService.dialogResult = false;
          this.loadAdmin = false;
          this.openErrorSnackBar(error.status + ': HTTP ERROR IN ADD ADMIN');
        });
      } else if (this.dialogState === 1) {
        // add admin
        const body = {
          firstName: this.data.first_name_text,
          lastName: this.data.last_name_text,
          countryCode: 91,
          phoneNumber: this.data.contact_number_text,
          email: this.data.email_text,
        };
        this.service.addAdmins(body).subscribe(success => {
          if (success.status) {
            AdminService.dialogResult = true;
            this.thisDialogRef.close();
            this.openSuccessSnackBar(success.message);
          } else {
            AdminService.dialogResult = false;
            this.openErrorSnackBar(success.message);
          }
          this.loadAdmin = false;
        }, error => {
          AdminService.dialogResult = false;
          this.loadAdmin = false;
          this.openErrorSnackBar(error.status + ': HTTP ERROR IN ADD ADMIN');
        });
      }
    }
  }

  isValid(): boolean {
    if (this.data.first_name_text === null || this.data.first_name_text === '') {
      this.openErrorSnackBar('Enter First Name');
      return false;
    } else {
      this.data.first_name_text = this.data.first_name_text.replace(
        this.data.first_name_text[0],
        this.data.first_name_text[0].toUpperCase()
      );
    }
    if (this.data.last_name_text === null || this.data.last_name_text === '') {
      this.openErrorSnackBar('Enter Last Name');
      return false;
    } else {
      this.data.last_name_text = this.data.last_name_text.replace(
        this.data.last_name_text[0],
        this.data.last_name_text[0].toUpperCase()
      );
    }
    if (this.data.contact_number_text === null || this.data.contact_number_text === '') {
      this.openErrorSnackBar('Enter a Contact Number');
      return false;
    } else if (this.data.contact_number_text.toString().length < 10) {
      this.openErrorSnackBar('Enter a valid Contact Number');
      return false;
    }
    if (this.data.email_text === null || this.data.email_text === '') {
      this.openErrorSnackBar('Enter a Email ID');
      return false;
    } else if (!this.data.email_text.includes('@' && '.')) {
      this.openErrorSnackBar('Enter a valid Email ID');
      return false;
    } else {
      this.data.email_text = this.data.email_text.replace(
        this.data.email_text,
        String(this.data.email_text).toLowerCase()
      );
    }
    if (this.dialogState === 1) {
      if (this.data.password === null || this.data.password.length === 0) {
        this.openErrorSnackBar('Enter a Password');
        return false;
      } else if (this.data.password.length < 8) {
        this.openErrorSnackBar('Password must have at least 8 characters');
        return false;
      }
    }
    return true;
  }

  openErrorSnackBar(message: string, ) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 5000;
    this.snackBar.open(message, 'Close', config);
  }

  openSuccessSnackBar(message: string, ) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-success'];
    config.duration = 3000;
    this.snackBar.open(message, 'Close', config);
  }

  isMoValid() {
    if (this.data.contact_number_text !== null) {
      let contact = this.data.contact_number_text.toString();
      if (contact.length >= 10) {
        contact = contact.substring(0, 9);
        this.data.contact_number_text = parseInt(contact, 10);
      }
    }
  }
}
