import { Component, OnInit, Inject } from '@angular/core';
import { MatSnackBar, MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import * as html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import * as moment from 'moment';

@Component({
  selector: 'app-appointments-preview',
  templateUrl: './appointments-preview.component.html',
  styleUrls: ['./appointments-preview.component.scss']

})

export class AppointmentsPreviewComponent implements OnInit {

  data: any;

  constructor(public thisDialogRef: MatDialogRef<AppointmentsPreviewComponent>,
    @Inject(MAT_DIALOG_DATA) private dialogData: any, private snackBar: MatSnackBar,
    public dialog: MatDialog) {
    this.dialogData = JSON.stringify(this.dialogData);
    this.dialogData = JSON.parse(this.dialogData);
    this.data = this.dialogData.dialog_data;
    this.loadOrdersData(this.data);
  }

  ngOnInit() {

  }

  loadOrdersData(data: any) {
    //console.log("load order data",data)
    //if (data !== undefined || this.data !== null) {
      if (data !== undefined && data !== null
        && data.length !== 0) {
       //   console.log("load order data",data.length)
        for (let i = 0; i < data.length; i++) {
         // console.log("load order data",data.length)
          if (data[i].requestedTime === undefined || data[i].requestedTime === 0 ||
            data[i].requestedTime === '') {
            data[i].requestedDateTime_text = 'N/A';
          } else {
            data[i].requestedDateTime_text = moment.unix(data[i].requestedTime / 1000000)
            .format(' hh:mm A DD/MM/YYYY');
          }
          if (data[i].booktime === undefined || data[i].booktime === 0 ||
            data[i].booktime === '') {
            data[i].bookingDateTime_text = 'N/A';
          } else {
            data[i].bookingDateTime_text = moment.unix(data[i].booktime / 1000000)
            .format(' hh:mm A DD/MM/YYYY');
          }
          if (data[i].accountDetails.length === undefined || data[i].accountDetails.length === 0 ||
            data[i].accountDetails[0].firstName === '' ||
            data[i].accountDetails[0].lastName === '') {
            data[i].fullName_text = 'N/A';
          } else {
            data[i].fullName_text = data[i].accountDetails[0].firstName + ' ' +
            data[i].accountDetails[0].lastName;
          }
          if (data[i].accountDetails.length === 0 ||
            data[i].accountDetails[0].contact.length === undefined ||
            data[i].accountDetails[0].contact.length === 0) {
              data[i].contact_number_text = 'N/A';
          } else {
            data[i].contact_number_text = data[i].accountDetails[0].contact[0].value;
          }
          if (data[i].accountDetails[0].contact.length === undefined ||
            data[i].accountDetails[0].contact.length === 0 ||
            data[i].accountDetails[0].contact.length < 2) {
              data[i].email_text = 'N/A';
          } else {
            data[i].email_text = data[i].accountDetails[0].contact[1].value;
          }
          if (data[i].serviceDetails.length === undefined || data[i].serviceDetails.length === 0 ||
            data[i].serviceDetails[0].serNameEnglish === '') {
            data[i].serviceNameEnglish_text = 'N/A';
          } else {
            data[i].serviceNameEnglish_text = data[i].serviceDetails[0].serNameEnglish;
          }
          if (data[i].stage === undefined || data[i].stage === null ||
            data[i].stage === '') {
            data[i].stage_text = 'N/A';
          } else {
            data[i].stage_text = data[i].stage;
          }
          if (data[i].session === undefined || data[i].session === null ||
            data[i].session === '') {
            data[i].session = 'N/A';
          } else {
            data[i].session = data[i].session;
          }
          if (data[i].serviceDetails.length === undefined || data[i].serviceDetails.length === 0 ||
            data[i].serviceDetails[0].serTATotal === '') {
            data[i].serviceDetails[0].serTATotal = 'N/A';
          } else {
            data[i].serviceTotal = data[i].serviceTotal;
          }
        }
        /*
        data.push(
        {
          sl_no: 'Grand Total',
          itemName_text: '---',
          description_text: '---',
          quantity_text: '---',
          itemCost_text: '---',
          itemTotal_text: data.grandTotal_text + '/-'
        }
      );*/
    }
    this.data = data;
  }


  onClose(): void {
    this.thisDialogRef.close();
  }

  onDownload(): void {
    const cntx = this;
    html2canvas.default(document.getElementById('orderSummaryContent')).then(function (canvas) {
     // console.log("download",cntx)
      const pdf = new jsPDF;
     // console.log("pdf")
      const img = canvas.toDataURL('image/jpeg');
     // console.log("img",cntx.data)
      pdf.addImage(img, 'PNG', 0, 0, 210, 297);
      pdf.save(cntx.data.id + '.pdf');
    });
  }
}
