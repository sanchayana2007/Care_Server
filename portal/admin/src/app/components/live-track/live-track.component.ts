import { Component, OnInit } from '@angular/core';
import { LiveTrackService } from './live-track.service';
import { SharedModule } from '../../../app/shared/shared.module';
import { GoogleLatLngBoundBuilder } from 'src/app/other/GoogleLatLngBoundBuilder';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { ObservableMedia, MediaChange } from '@angular/flex-layout';
import * as _moment from 'moment';
const moment = (_moment as any).default ? (_moment as any).default : _moment;
@Component({
  selector: 'app-live-track',
  templateUrl: './live-track.component.html',
  styleUrls: ['./live-track.component.scss'],
  providers: [LiveTrackService]
})
export class LiveTrackComponent implements OnInit {

  vehicleData: any;
  vehicleMarkers: Array<any> = [];
  selectedvehicleData: Array<any> = [];
  selectedvehicleMarkers: Array<any> = [];
  selectedvehicleMarkerPaths: Array<any> = [];
  googleMap: any;
  wsSocket: any;
  googleMapLoaded = false;
  getData = true;
  layoutAlign = 'row';
  listMaxHeight = '100%';
  gMapMaxHeight = '100%';
  DATE_TIME_FORMAT = 'MM/DD/YY hh:mm:ss a';

  constructor(private service: LiveTrackService,
    private media: ObservableMedia) {
    this.media.subscribe((mediaChange: MediaChange) => {
      if (this.media.isActive('gt-md')) {
        this.listMaxHeight = '100%';
        this.gMapMaxHeight = '100%';
        this.layoutAlign = 'row';
      } else if (this.media.isActive('gt-xs')) {
        this.listMaxHeight = '100%';
        this.gMapMaxHeight = '100%';
        this.layoutAlign = 'row';
      } else if (this.media.isActive('lt-sm')) {
        this.listMaxHeight = '30%';
        this.gMapMaxHeight = '70%';
        this.layoutAlign = 'column';
      } else if (this.media.isActive('xs')) {
        this.listMaxHeight = '30%';
        this.gMapMaxHeight = '70%';
        this.layoutAlign = 'column';
      }
    });
    this.wsSocket = SharedModule.GWwebSocket;
    this.wsSocket.onmessage = msg => this.sendToSwitch(msg.data);
  }

  ngOnInit() {
    ToolbarHelpers.toolbarTitle = 'Live Track';
    this.initMap();
    // this.Map();
  }

  initMap() {
    this.googleMap = new google.maps.Map(document.getElementById('google_map_canvas'), {
      center: { lat: 23.829321, lng: 91.277847 },
      zoom: 8
    });
    const cntx = this;
    this.googleMap.addListener('tilesloaded', event => {
      if (!cntx.googleMapLoaded) {
        cntx.getLiveVehicle();
        cntx.googleMapLoaded = true;
      }
    });
  }
  Map() {
    this.googleMap = new google.maps.Map(document.getElementById('google_map'), {
      center: { lat: 23.829321, lng: 91.277847 },
      zoom: 8
    });
    const cntx = this;
    this.googleMap.addListener('tilesloaded', event => {
      if (!cntx.googleMapLoaded) {
        cntx.getLiveVehicle();
        cntx.googleMapLoaded = true;
      }
    });
  }


  getLiveVehicle() {
    this.service.getVehicles().subscribe(success => {
        if (success.status) {
          this.loadVehicleData(success.result);
        }
      },
      error => {
      }
    );
  }

  loadVehicleData(data: any): void {
    const latLngArray = [];
    this.clearVehicleMarkers();
    const cntx = this;
    const cTime = new Date().getTime();
    if (data !== undefined && data !== null && data.length !== 0) {
      for (let i = 0; i < data.length; i++) {
        const mLatLng = {
          lat: data[i].gps_data[0].latitude,
          lng: data[i].gps_data[0].longitude
        };
        const tDiff = cTime - data[i].gps_data[0].time;
        if (tDiff < 7200000) {
          data[i].state = 0;
        } else if (tDiff > 7200000 && tDiff < 21600000) {
          data[i].state = 1;
        } else {
          data[i].state = 2;
        }
        latLngArray.push(mLatLng);
        const mark = new google.maps.Marker({
          position: mLatLng,
          icon: '../../../assets/images/gcar.png',
          title: data[i].reg_num
        });
        let ign = 'OFF';
        if (data[i].gps_data[0].ignition) {
          ign = 'ON';
        }
        const textTime = moment.unix(data[i].gps_data[0].time / 1000).format(this.DATE_TIME_FORMAT);
        const infowindow = new google.maps.InfoWindow({
          content: '<p> Registration No: ' + data[i].reg_num + '</p>' +
            '<p> Time: ' + textTime + '</p>' +
            '<p> Ignition: ' + ign + '</p>'
        });
        mark.set('info', infowindow);
        mark.set('reg_num', data[i].reg_num);
        mark.addListener('click', function () {
          mark.get('info').open(cntx.googleMap, mark);
        });
        mark.setValues({ id: data[i].id });
        mark.setMap(this.googleMap);
        this.vehicleMarkers.push(mark);
      }
      GoogleLatLngBoundBuilder.setBounds(this.googleMap, latLngArray, 14);
      this.vehicleData = data;
    } else {
      this.vehicleData = [];
    }
  }

  onVehicleSelected(event: any) {
    let fState = true;
    const latLngArray = [];
    const msg = {
      msg_type: 'SUB_VEHICLE_STATUS',
      data: [
        {
          id: event.id
        }
      ]
    };
    // this.initMap();
    const cntx = this;
    if (this.selectedvehicleData.length > 0) {
      for (let i = 0; i < this.selectedvehicleData.length; i++) {
        const vehicle = this.selectedvehicleData[i];
        if (event.id === vehicle.id) {
          msg.msg_type = 'UNSUB_VEHICLE_STATUS',
            this.wsSocket.send(JSON.stringify(msg));
          this.selectedvehicleData.splice(i, 1);
          fState = false;
          this.getData = false;
        }
      }
      if (fState) {
        msg.msg_type = 'SUB_VEHICLE_STATUS';
        this.wsSocket.send(JSON.stringify(msg));
        this.selectedvehicleData.push(event);
        this.getData = false;
      }
    } else {
      msg.msg_type = 'SUB_VEHICLE_STATUS';
      this.wsSocket.send(JSON.stringify(msg));
      this.selectedvehicleData.push(event);
    }
    if (this.selectedvehicleData.length === 0) {
      this.loadVehicleData(this.vehicleData);
    } else {
      this.clearVehicleMarkers();
      this.clearSelectedVehicleMarkers();
      this.clearSelectedVehicleMarkerPaths();
      const data = this.selectedvehicleData;
      if (data !== undefined && data !== null && data.length !== 0) {
        for (let i = 0; i < data.length; i++) {
          const mLatLng = {
            lat: data[i].gps_data[0].latitude,
            lng: data[i].gps_data[0].longitude
          };
          latLngArray.push(mLatLng);
          const mark = new google.maps.Marker({
            position: mLatLng,
            icon: '../../../assets/images/gcar.png',
            title: data[i].reg_num
          });
          let ign = 'OFF';
          if (data[i].gps_data[0].ignition) {
            ign = 'ON';
          }
          const textTime = moment.unix(data[i].gps_data[0].time / 1000)
            .format(this.DATE_TIME_FORMAT);
          const infowindow = new google.maps.InfoWindow({
            content: '<p> Registration No: ' + data[i].reg_num + '</p>' +
              '<p> Time: ' + textTime + '</p>' +
              '<p> Ignition: ' + ign + '</p>'
          });
          mark.set('info', infowindow);
          mark.set('reg_num', data[i].reg_num);
          mark.addListener('click', function () {
            mark.get('info').open(cntx.googleMap, mark);
          });
          mark.setValues({ id: data[i].id });
          mark.setMap(this.googleMap);
          const markPath = new google.maps.Polyline({
            path: [],
            geodesic: true,
            strokeColor: '#1BD520',
            strokeOpacity: 1.0,
            strokeWeight: 2
          });
          markPath.setValues({ id: data[i].id });
          markPath.setMap(this.googleMap);
          this.selectedvehicleMarkerPaths.push(markPath);
          this.selectedvehicleMarkers.push(mark);
        }
        GoogleLatLngBoundBuilder.setBounds(this.googleMap, latLngArray, 14);
      }
    }
  }

  clearVehicleMarkers() {
    for (let i = 0; i < this.vehicleMarkers.length; i++) {
      this.vehicleMarkers[i].setMap(null);
    }
    this.vehicleMarkers = [];
  }

  clearSelectedVehicleMarkers() {
    for (let i = 0; i < this.selectedvehicleMarkers.length; i++) {
      this.selectedvehicleMarkers[i].setMap(null);
    }
    this.selectedvehicleMarkers = [];
  }

  clearSelectedVehicleMarkerPaths() {
    for (let i = 0; i < this.selectedvehicleMarkerPaths.length; i++) {
      this.selectedvehicleMarkerPaths[i].setMap(null);
    }
    this.selectedvehicleMarkerPaths = [];
  }

  sendToSwitch(message: string): void {
    message = message.replace(/'/g, '"');
    const msg = JSON.parse(message);
    if (msg.msg_type === 'conn_ready') {
    } else {
      switch (msg.msg_type) {
        case 'PUB_VEHICLE_STATUS':
          const mLatLng = {
            lat: msg.data[0].latitude,
            lng: msg.data[0].longitude
          };
          if (this.selectedvehicleMarkers.length !== 0) {
            for (let i = 0; i < this.selectedvehicleMarkers.length; i++) {
              if (this.selectedvehicleMarkers[i].get('id') === msg.data[0].id) {
                this.selectedvehicleMarkers[i].setPosition(mLatLng);
                let ign = 'OFF';
                if (msg.data[0].ignition) {
                  ign = 'ON';
                }
                const textTime = moment.unix(msg.data[0].time / 1000).format(this.DATE_TIME_FORMAT);
                const infowindow = new google.maps.InfoWindow({
                  content: '<p> Registration No: ' +
                    this.selectedvehicleMarkers[i].get('reg_num') + '</p>' +
                    '<p> Time: ' + textTime + '</p>' +
                    '<p> Ignition: ' + ign + '</p>'
                });
                this.selectedvehicleMarkers[i].set('info', infowindow);
                break;
              }
            }
          }
          if (this.selectedvehicleMarkerPaths.length !== 0) {
            for (let i = 0; i < this.selectedvehicleMarkerPaths.length; i++) {
              if (this.selectedvehicleMarkerPaths[i].get('id') === msg.data[0].id) {
                const latLngArr = this.selectedvehicleMarkerPaths[i]
                  .getPath().getArray();
                latLngArr.push(mLatLng);
                this.selectedvehicleMarkerPaths[i].setPath(latLngArr);
                let ign = 'OFF';
                if (msg.data[0].ignition) {
                  ign = 'ON';
                }
                const textTime = moment.unix(msg.data[0].time / 1000).format(this.DATE_TIME_FORMAT);
                const infowindow = new google.maps.InfoWindow({
                  content: '<p> Registration No: ' +
                    this.selectedvehicleMarkers[i].get('reg_num') + '</p>' +
                    '<p> Time: ' + textTime + '</p>' +
                    '<p> Ignition: ' + ign + '</p>'
                });
                this.selectedvehicleMarkers[i].set('info', infowindow);
                break;
                break;
              }
            }
          }
          break;
        default:
          break;
      }
    }
  }

}
