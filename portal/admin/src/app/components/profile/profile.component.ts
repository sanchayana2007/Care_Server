import { ElementCoreService } from './../../element-core/element-core.service';
import { Component, OnInit, Inject } from '@angular/core';
import {
  MatDialogRef, MAT_DIALOG_DATA,
  MatSnackBarConfig, MatSnackBar
} from '@angular/material';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
  providers: [ElementCoreService]
})
export class ProfileComponent implements OnInit {

  data: any;
  title: string;
  file_name: any;
  url: string;
  form: any;
  file: any;
  key: any;
  storage: any;
  loading: any;
  DriverService: any;
  image: Blob;
  picture_upload_title = '';

  constructor(public thisDialogRef: MatDialogRef<ProfileComponent>,
    @Inject(MAT_DIALOG_DATA) private dailogData: any,
    private snackBar: MatSnackBar, private service: ElementCoreService) {
    this.dailogData = JSON.stringify(this.dailogData);
    this.dailogData = JSON.parse(this.dailogData);
    this.data = this.dailogData.dialog_data;
    if (this.data) {
      this.title = 'Edit Profile Details';
      this.picture_upload_title = 'Change Picture';
      const f_name = this.data.full_name.split(' ');
      this.data.first_name = f_name[0];
      this.data.image_url = this.data.files[0].profile;
      this.data.last_name = f_name[1];
      this.data.phone_number = this.data.phone_number;
    } else {
    }
  }

  ngOnInit() {
  }

  onClose(): void {
    this.thisDialogRef.close();
  }

}
