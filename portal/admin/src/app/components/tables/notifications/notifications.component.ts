import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { MatSnackBarConfig, MatSnackBar } from '@angular/material/snack-bar';
import { environment } from '../../../../environments/environment';
import {NotificationsService} from './notifications.service';
import { from } from 'rxjs';
@Component({
  selector: 'app-admin',
  templateUrl: './notifications.component.html',
  styleUrls: ['./notifications.component.scss'],
  providers: [NotificationsService]
})
export class NotificationsComponent implements OnInit {
  fileName: any;
  serviceType = 0;
  nextButton = false;
  data: any;
  submitButton = true;
  loadImage = false;
  defaultImage = environment.proxyApiUrl + '/uploads/img_place_holder.png';
  imageList: Array<any> = [
    {
      slNo: 1,
      imgName: 'Upload Document Image ',
      idProof: null,
      fileUrl: this.defaultImage,
      fileLink: '',
      fileSelected: false
    },
  ];

  constructor(private router: Router, private service: NotificationsService,
              private snackBar: MatSnackBar, private activatedRoute: ActivatedRoute
  ) {

  }
  ngOnInit(): void {
  }

  getTourTransport(): void {
    this.service.getTourTransport(this.serviceType).subscribe(success => {
      const image = success.result;
      this.imageList[0].fileUrl = image[0].document[0].link;
      this.imageList[1].fileUrl = image[0].declaration[0].link;
    }
    );
  }

  documentUpload(event: any, index: number): void {
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (events: any) => {
        this.imageList[index].fileUrl = events.target.result;
      };
    }
    const fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      const file: File = fileList[0];
      const formData: FormData = new FormData();
      const filename = file.name;
      this.fileName = filename.substring(filename.lastIndexOf('/'));
      formData.append('idProof', file, filename);
      // formData.append('idProof1', file, filename);
      this.imageList[index].idProof = formData;
      // this.imageData.push({ 'method': 1, 'image': formData });
    } else {
      this.imageList[index].idProof = null;
    }
  }

  onImageSubmit(): void {
        this.service.secondtImageSubmit
        (this.imageList[1].idProof, this.data).subscribe(success => {
          if (success.status) {
            this.openSuccessSnackBar(success.message);
            setTimeout(() => {
              location.replace(environment.proxyApiUrl);
            }, 300);
          } else {
            this.openErrorSnackBar(success.message);
          }
    });
  }
  uploadTrigger0(): void {
    this.imageList[0].fileSelected = true;
    document.getElementById('upload0').click();
  }
  uploadTrigger1(): void {
    this.imageList[1].fileSelected = true;
    document.getElementById('upload1').click();
  }

  openDefaultSnackBar(message: string): void {
    const config = new MatSnackBarConfig();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-default'];
    config.duration = 800;
    this.snackBar.open(message, 'Close', config);
  }

  openSuccessSnackBar(message: string, ): void {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'center';
    config.panelClass = ['snakbar-class-success'];
    config.duration = 3000;
    this.snackBar.open(message, 'Close', config);
  }

  openErrorSnackBar(message: string, ): void {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 5000;
    this.snackBar.open(message, 'Close', config);
  }
}

