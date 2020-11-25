import { Component, OnInit } from '@angular/core';
import { MatSnackBarConfig, MatSelectChange, MatSnackBar } from '@angular/material';
import { SmsService } from './sms.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sms',
  templateUrl: './sms.component.html',
  styleUrls: ['./sms.component.scss'],
  providers: [SmsService]
})
export class SmsComponent implements OnInit {
  count: any;
  loadSms = false;
  body: any;
  hideprovide = true;
  smsCredit: any;
  data = {
    selectedProvider: null,
    message_text: '',
    contact_text: '',
  };
  providerData = [
    {
      name: 'Providers',
      value: 1,
    },
    {
      name: 'Users',
      value: 0,
    },
  ];

  constructor(private snackBar: MatSnackBar, private service: SmsService,
    private router: Router) { }

  ngOnInit() {
    this.getcridets();
  }
  getcridets(): void {
    this.service.getSmsCreadits().subscribe(success => {
      console.log(success, 'credits');
      if ( success.status) {
        this.smsCredit = success.result[0].smsCredits;
      }
    });
  }
  onChange(event): void {
    if (event.checked === true) {
      this.hideprovide = false;
      this.count = 1;
    } else {
      this.hideprovide = true;
      this.count = 0;
    }
  }

  onProviderChange(event: MatSelectChange): void {
    for (let i = 0; i < this.providerData.length; i++) {
      const propretyData = this.providerData[i];
      if (event.value === propretyData.value) {
        this.data.selectedProvider = propretyData.value;
      }
    }
  }

  onSubmit() {
    if (this.isValid()) {
      this.loadSms = true;
      if (this.count === 1) {
        this.body = {
          smsMessage: this.data.message_text,
          manual: true,
          numbers: this.data.contact_text
        };
      } else {
        this.body = {
          serviceType: this.data.selectedProvider,
          smsMessage: this.data.message_text,
          manual: false,
        };
      }
      
      console.log(this.body);
      this.service.addSms(this.body).subscribe(success => {
        if (success.status) {
          this.openSuccessSnackBar(success.message);
          this.onRefresh();
        } else {
          this.openErrorSnackBar(success.message);
        }
        this.loadSms = false;
      }, error => {
        this.loadSms = false;
        this.openErrorSnackBar(error.status + ': HTTP ERROR IN ADD SMS');
      });
    }
  }

  onRefresh() {
    this.data.selectedProvider = '';
    this.data.message_text = '';
    this.data.contact_text = '';
  }

  isValid(): boolean {
    if (this.data.selectedProvider === null ) {
      this.openErrorSnackBar('Select service provider');
      return false;
    }
    if (this.data.message_text === null || this.data.message_text === '') {
      this.openErrorSnackBar('Enter some message');
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
    config.duration = 5000;
    this.snackBar.open(message, 'Close', config);
  }
}

