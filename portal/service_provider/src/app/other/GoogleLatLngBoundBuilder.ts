export class GoogleLatLngBoundBuilder {

  public static setBounds(googleMap: any, latlngBoundArray: any, zoomLevel: number): boolean {
    let latlngBounds = null;
    latlngBounds = new google.maps.LatLngBounds();
    if (latlngBoundArray.length > 0) {
      for (let i = 0; i < latlngBoundArray.length; i++) {
        latlngBounds.extend(latlngBoundArray[i]);
        googleMap.fitBounds(latlngBounds);
      }
      if (zoomLevel !== null) {
        googleMap.setZoom(zoomLevel);
      }
    } else {
      return false;
    }
    return true;
  }

}
