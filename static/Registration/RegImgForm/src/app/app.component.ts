import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { MatSnackBarConfig, MatSnackBar } from '@angular/material/snack-bar';
import { AppService } from './app.service';
import { environment } from '../environments/environment';
import * as html2canvas from 'html2canvas';
import { default as JSPDF } from 'jspdf';
import { HttpClientModule, HttpClient, HttpRequest, HttpResponse, HttpEventType } from '@angular/common/http';
import { nonWhiteSpace } from 'html2canvas/dist/types/css/syntax/parser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [AppService]
})
export class AppComponent implements OnInit {
  fileName: any;
  serviceType = 0;
  data: any;
  image: any;
  nextButton = false;
  loadImage = false;
  districts: any;
  defaultImage = environment.proxyApiUrl + '/uploads/img_place_holder.png';
  imageList: Array<any> = [
    {
      slNo: 1,
      imgName: 'Profile Picture ',
      idProof: null,
      fileUrl: this.defaultImage,
      fileLink: '',
      fileSelected: false
    },
    {
      slNo: 2,
      imgName: 'Document',
      idProof: null,
      fileUrl: this.defaultImage,
      fileLink: '',
      fileSelected: false
    },
    {
      slNo: 3,
      imgName: 'Declaration',
      idProof: null,
      fileUrl: this.defaultImage,
      fileLink: '',
      fileSelected: false
    },
    {
      slNo: 4,
      imgName: 'Signature',
      idProof: null,
      fileUrl: this.defaultImage,
      fileLink: '',
      fileSelected: false
    }
  ];
  pincode: any;
  serviceList = [];
  services: any;
  areaofoperation: any;
  srvList = [];
  pinCodes: any;
  download: any;
  State: any;
  documentUploads = new FormData();
  constructor(private router: Router, private service: AppService, private http: HttpClient,
    private snackBar: MatSnackBar, private activatedRoute: ActivatedRoute
  ) {
    this.data = {};
    this.data.address = '';
    this.data.serviceList = [];
    this.data.qualification = '';
    this.data.areaofoperation = [];
    this.data.state = '';
    this.data.district = '';
    this.data.checkbox = '';
    this.services = [];
    this.areaofoperation = [];
    this.srvList = [];
    this.State = [];
  }
  ngOnInit(): void {
    setTimeout(() => {
      this.activatedRoute.queryParams.subscribe(params => {
        // let date = params['startdate'];
        if (params !== null && params.toString() !== '') {
          this.service.updateToken(
            params['Authorization'],
            params['x-Origin-Key'],
            params['x-Api-Key'],
            params['id']
          );
          this.serviceType = parseInt(params['serviceType']);
          this.getServices();
          this.getServicesList();
          this.getStateList();
        }
      });
    }, 300);

  }
  // onDownload(): void {
  //   this.nextButton = true;
  //   const cntx = this;
  //   html2canvas.default(document.getElementById('image')).then(function (canvas) {
  //     // console.log("download",cntx)
  //     const pdf = new JSPDF();
  //     // const pdf = new jsPDF();
  //     console.log(pdf);
  //     const img = canvas.toDataURL('image/jpeg');
  //     // console.log("img",cntx.data)
  //     pdf.addImage(img, 0, 0, 0, 0);
  //     pdf.save('image' + '.pdf');
  //   });
  //   this.nextButton = false;
  // }

  getServicesList(): void {
    this.service.getService_list().subscribe(data => {
      if (data.status) {
        this.serviceList = data.result;
      }
    });
  }
  getStateList(): void {
    this.service.getState().subscribe(data => {
      if (data.status) {
        this.State = data.result;
      }
    });
  }
  onDistrictsChange(districtName): void {
    this.getAreaList(districtName);
  }
  onStateChange(stateName): void {
    this.getDistrictsList(stateName);
  }

  getDistrictsList(stateName): void {
    this.service.getDistricts(stateName).subscribe(data => {
      if (data.status) {
        this.districts = data.result;
      }
    });
  }
  onChange(districtName): void {
    this.getAreaList(districtName);
  }
  getAreaList(districtName): void {
    this.service.getAreas(districtName).subscribe(data => {
      if (data.status) {
        this.pincode = data.result;
      }
    });
  }

  onClickHandler(cb): void {
    this.data.checkbox = cb.checked;
  }
  getServices(): void {
    this.service.getServices(this.serviceType).subscribe(success => {
      if (success.status) {
        this.image = success.result;
        this.download = this.image[0].document[0].link;
        this.imageList[0].fileUrl = this.image[0].profilePic[0].link;
        this.imageList[1].fileUrl = this.image[0].declaration[0].link;
        this.imageList[2].fileUrl = this.image[0].document[0].link;
        this.imageList[3].fileUrl = this.image[0].signature[0].link;
        this.data.address = this.image[0].address;
        this.data.district = this.image[0].district;
        this.data.state = this.image[0].state;
        this.data.checkbox = this.image[0].terms;
        this.data.qualification = this.image[0].qualification;
        this.pinCodes = this.image[0].areaOfOperation;
        const dummy = [];
        for (let i = 0; i < this.pinCodes.length; i++) {
          dummy.push(Number(this.pinCodes[i]));
        }
        for (let i = 0; i < this.image[0].serviceList.length; i++) {
          this.services.push(this.image[0].serviceList[i].serviceId);
          this.srvList.push(this.image[0].serviceList[i].serviceName);
        }

        this.data.areaofoperation = dummy;
        this.data.serviceList = this.srvList;
      }
      this.onStateChange(this.data.state);
      setTimeout(() => {
        this.onDistrictsChange(this.data.district);
      }, 300);
    }
    );

  }
  documentUploadOne(event: any): void {
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (events: any) => {
        this.imageList[0].fileUrl = events.target.result;
      };
    }
    const fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      const file: File = fileList[0];
      const formData: FormData = new FormData();
      const filename = file.name;
      this.fileName = filename.substring(filename.lastIndexOf('/'));
      formData.append('id1Proof', file, filename);
      this.imageList[0].id1Proof = formData;
      this.imageList[0].file = file;
      this.imageList[0].fileName = filename;
    } else {
      this.imageList[0].id1Proof = null;
    }
  }

  documentUploadTwo(event: any): void {
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (events: any) => {
        this.imageList[1].fileUrl = events.target.result;
      };
    }
    const fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      const file: File = fileList[0];
      const formData: FormData = new FormData();
      const filename = file.name;
      this.fileName = filename.substring(filename.lastIndexOf('/'));
      formData.append('id2Proof', file, filename);
      this.imageList[1].id2Proof = formData;
      this.imageList[1].file = file;
      this.imageList[1].fileName = filename;
    } else {
      this.imageList[1].id2Proof = null;
    }
  }

  documentUploadThree(event: any): void {
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (events: any) => {
        this.imageList[2].fileUrl = events.target.result;
      };
    }
    const fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      const file: File = fileList[0];
      const formData: FormData = new FormData();
      const filename = file.name;
      this.fileName = filename.substring(filename.lastIndexOf('/'));
      formData.append('', file, filename);
      this.imageList[2].liveProof = formData;
      this.imageList[2].file = file;
      this.imageList[2].fileName = filename;
    } else {
      this.imageList[2].liveProof = null;
    }
  }
  documentUploadFour(event: any): void {
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (events: any) => {
        this.imageList[3].fileUrl = events.target.result;
      };
    }
    const fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      const file: File = fileList[0];
      const formData: FormData = new FormData();
      const filename = file.name;
      this.fileName = filename.substring(filename.lastIndexOf('/'));
      formData.append('', file, filename);
      this.imageList[3].liveProof = formData;
      this.imageList[3].file = file;
      this.imageList[3].fileName = filename;
    } else {
      this.imageList[3].liveProof = null;
    }
  }
  Onselect(data, value, event): void {
      if (value === 1 && event.source._selected === true) {
        this.services.push(data._id);
      } else if (value === 1 && event.source._selected === true) {
        this.services.pop();
      }


  }

  onImageSubmit(): void {
    const queryParams = {
      qualification: this.data.qualification,
      district: this.data.district,
      state: this.data.state,
      address: this.data.address,
      terms: this.data.checkbox
    };
    this.documentUploads = new FormData();
    this.documentUploads.append
      ('profilePic', this.imageList[0].file);
    this.documentUploads.append
      ('document', this.imageList[1].file);
    this.documentUploads.append
      ('declaration', this.imageList[2].file);
    this.documentUploads.append
      ('signature', this.imageList[3].file);
    this.documentUploads.append
      ('serviceList', this.services);
    this.documentUploads.append
      ('areaOfOperation', this.data.areaofoperation);

    this.service.postData(queryParams, this.documentUploads
    ).subscribe(
      success => {
        if (success.status) {
          this.openSuccessSnackBar(success.message);
          setTimeout(() => {
            // location.replace(environment.dashboardUrl);
          }, 300);
        } else {
          this.openErrorSnackBar(success.message);
        }
      });
    return;
  }

  uploadTrigger0(): void {
    this.imageList[0].fileSelected = true;
    document.getElementById('upload0').click();
  }
  uploadTrigger1(): void {
    this.imageList[1].fileSelected = true;
    document.getElementById('upload1').click();
  }
  uploadTrigger2(): void {
    this.imageList[2].fileSelected = true;
    document.getElementById('upload2').click();
  }
  uploadTrigger3(): void {
    this.imageList[3].fileSelected = true;
    document.getElementById('upload3').click();
  }

  openDefaultSnackBar(message: string): void {
    const config = new MatSnackBarConfig();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-default'];
    config.duration = 800;
    this.snackBar.open(message, 'Close', config);
  }

  openSuccessSnackBar(message: string): void {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'center';
    config.panelClass = ['snakbar-class-success'];
    config.duration = 3000;
    this.snackBar.open(message, 'Close', config);
  }

  openErrorSnackBar(message: string): void {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 5000;
    this.snackBar.open(message, 'Close', config);
  }
}


