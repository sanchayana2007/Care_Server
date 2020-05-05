import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { ServiceListService } from '../service-list.service';

@Component({
  selector: 'app-service-image-upload-dialog',
  templateUrl: './service-image-upload-dialog.component.html',
  styleUrls: ['./service-image-upload-dialog.component.scss'],
  providers: [ServiceListService]
})
export class ServiceImageUploadDialogComponent implements OnInit {

  data: any;
  title: string;
  file_name: any;
  loadServiceImage = false;
  dialogState = 0;
  formData: any = null;

  constructor(public thisDialogRef: MatDialogRef<ServiceImageUploadDialogComponent>,
    @Inject(MAT_DIALOG_DATA) private dailogData: any, private snackBar: MatSnackBar,
    private service: ServiceListService) {
    this.dailogData = JSON.stringify(this.dailogData);
    this.dailogData = JSON.parse(this.dailogData);
    this.data = this.dailogData.dialog_data;
    this.title = 'Service Image Upload';

    if (this.data !== null) {
      if (this.data.serviceImage !== '') {
        this.data.image_url = this.data.serviceImage;
      } else {
        this.data.image_url = this.data.serviceImage;
      }
    }
  }

  ngOnInit() {

  }

  onClose(): void {
    ServiceListService.dialogResult = false;
    this.thisDialogRef.close();
  }

  image_upload_trigger() {
    document.getElementById('upload').click();
  }

  serviceImageUpload(event: any) {
    this.loadServiceImage = true;
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (events: any) => {
        this.loadServiceImage = false;
        this.data.image_url = events.target.result;
      };
    }
    const fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      const file: File = fileList[0];
      const formData: FormData = new FormData();
      const filename = file.name;
      this.file_name = filename.substring(filename.lastIndexOf('/'));
      formData.append('file', file, filename);
      this.formData = formData;
    }
  }

  onSave() {
    if (this.formData === null) {
      this.openErrorSnackBar('Please Select an Image.');
      return;
    }
    this.loadServiceImage = true;
    const id = this.data.id;
    const body = {
      serviceMedia: this.data.image_url,
    };
    this.service.uploadServiceImage(id, body).subscribe(
      success => {
        if (success.status) {
          this.thisDialogRef.close();
          this.openSuccessSnackBar(success.message);
        } else {
          this.openErrorSnackBar(success.message);
        }
        this.loadServiceImage = false;
      },
      error => {
        this.openErrorSnackBar('HTTP ERROR');
        this.loadServiceImage = false;
      }
    );
  }

  openErrorSnackBar(message: string) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 5000;
    this.snackBar.open(message, 'Close', config);
  }

  openSuccessSnackBar(message: string) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-success'];
    config.duration = 3000;
    this.snackBar.open(message, 'Close', config);
  }
}
