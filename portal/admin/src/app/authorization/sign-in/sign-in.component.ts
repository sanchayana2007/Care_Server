import { Component, OnInit } from '@angular/core';
import { AUTHGWCONSTANTS } from '../authconstants';
import { Router } from '@angular/router';
import { AuthorizationService } from '../authorization.service';
import { MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss'],
  providers: [AuthorizationService]
})
export class SignInComponent implements OnInit {

  passwordHide = true;
  user_id = '';
  password = '';
  curr_focus = '';

  constructor(private authService: AuthorizationService, private router: Router,
    private snackBar: MatSnackBar) { }

  ngOnInit() {
    const the = this;
    document.addEventListener('keypress', function (event: any) {
      if (event.keyCode === 13) {
        if (the.curr_focus === 'u_id') {
          document.getElementById('pass').focus();
        } else if (the.curr_focus === 'password') {
          the.sign_in();
        }
      }
    });
  }

  sign_in() {
    if (this.getErrorMessage()) {
      const body = {
        username: this.user_id,
        password: this.password,
        applicationId: environment.applicationId,
        method: 0
      };
      this.authService.postSignIn(body).subscribe(success => {
        if (success.status) {
          localStorage.setItem(AUTHGWCONSTANTS.bearerToken, success.result[0].bearerToken);
          localStorage.setItem(AUTHGWCONSTANTS.xApiKey, success.result[0].apiKey);
          if (this.authService.updateHeaders()) {
            this.router.navigate(['admin/dashboard']);
            this.openSuccessSnackBar(success.message);
          } else {
            this.openErrorSnackBar(success.message);
          }
          // TODO: for Access Origin Key
          // localStorage.setItem(AUTHGWCONSTANTS.bearerToken, success.result[0].bearerToken);
        } else {
          this.openErrorSnackBar(success.message);
        }
      });
    } else {
    }
  }

  getErrorMessage(): boolean {
    if (this.user_id === '') {
      this.openErrorSnackBar('Enter your User ID');
      // document.getElementById('error_msg').innerText = 'Enter your User ID*';
      return false;
    }
    if (this.password === '') {
      this.openErrorSnackBar('Enter your Password');
      // document.getElementById('error_msg').innerText = 'Enter your Password*';
      return false;
    }
    return true;
  }

  openSuccessSnackBar(message: string, ) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-success'];
    config.duration = 3000;
    this.snackBar.open(message, 'Close', config);
  }

  openErrorSnackBar(message: string, ) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 3000;
    this.snackBar.open(message, 'Close', config);
  }
}

