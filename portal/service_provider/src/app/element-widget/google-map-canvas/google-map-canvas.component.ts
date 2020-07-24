import { Component, OnInit } from '@angular/core';
import { GoogleMapLoaderService } from 'src/app/other/GoogleMapLoader';

@Component({
  selector: 'app-google-map-canvas',
  templateUrl: './google-map-canvas.component.html',
  styleUrls: ['./google-map-canvas.component.scss']
})
export class GoogleMapCanvasComponent implements OnInit {

  // googleMap: any;

  data: any;
  title: string;
  googleMap: any;
  tripPointmarker: any = null;
  geocoderService: any;
  loadTripPoint = false;
  dialogState = 0;

  constructor() { }

  ngOnInit() {
    this.initMap();
  }

  initMap() {
    const context = this;
    // this.geocoderService = new google.maps.Geocoder;
    GoogleMapLoaderService.load().then(() => {
      this.googleMap = new google.maps.Map(document.getElementById('google_map_canvas'), {
        center: { lat: 23.8294379, lng: 91.2785561 },
        zoom: 12,
        scrollwheel: false
      });
      this.googleMap.addListener('tilesloaded', event => {
        context.onMapLoaded();
      });
    });
  }

  // initMap() {
  //   const context = this;
  //   this.geocoderService = new google.maps.Geocoder;
  //   this.googleMap = new google.maps.Map(document.getElementById('google_map_canvas'), {
  //     center: { lat: 23.8294379, lng: 91.2785561 },
  //     zoom: 12
  //   });
  //   this.googleMap.addListener('tilesloaded', event => {
  //     context.onMapLoaded();
  //   });
  // }

  onMapLoaded() {
    const context = this;
    this.googleMap.addListener('click', event => {
      // console.log(event);
      const latLng = JSON.parse(JSON.stringify(event.latLng));
      // console.log(latLng);
      // context.data.latitude_text = latLng.lat;
      // context.data.longitude_text = latLng.lng;
      context.placeTripPointMarker(latLng);
    });
  }

  placeTripPointMarker(latLng: any): void {
    if (this.tripPointmarker === null) {
      this.tripPointmarker = new google.maps.Marker({
        position: latLng,
        map: this.googleMap,
        // draggable: true,
      });
    } else  {
      this.tripPointmarker.setPosition(latLng);
    }
    const context = this;
    this.tripPointmarker.addListener('dragend', event => {
      const nlatLng = JSON.parse(JSON.stringify(event.latLng));
      // console.log(nlatLng);
      context.data.latitude_text = nlatLng.lat;
      context.data.longitude_text = nlatLng.lng;
    });
    this.googleMap.panTo(latLng);
    this.googleMap.setZoom(15);
  }

}
