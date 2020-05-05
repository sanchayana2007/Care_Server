import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AUTHGWCONSTANTS } from '../../../authorization/authconstants';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AppointmentsService {

  public static dialogResult = true;
  xOriginKey = environment.xOrigin.key;
  xApiKey = environment.xApi.key;
  headers: any;
  constructor(private http: HttpClient) {
    const token = localStorage.getItem(AUTHGWCONSTANTS.bearerToken);
    // const xOriginKey = localStorage.getItem(AUTHGWCONSTANTS.xOriginKey);
    // const xApiKey = localStorage.getItem(AUTHGWCONSTANTS.xApiKey);
    this.headers = {
      Authorization: 'Bearer ' + token,
      'x-Origin-Key': this.xOriginKey,
      'x-Api-Key': this.xApiKey,
    };
  }

  getAppointments(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/med/book', {
      headers: this.headers
    });
  }

  addAppointments(body): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
    '/web/api/med/update', body, {
      headers: this.headers
    });
  }

  editAppointments(body): Observable<any> {
    return this.http.put<any>(environment.proxyApiUrl +
    '/web/api/med/book', body, {
      headers: this.headers
    });
  }

  deleteAppointments(id): Observable<any> {
    return this.http.delete<any>(environment.proxyApiUrl +
    '/web/api/med/book?id=' + id, {
      headers: this.headers,
    });
  }
}

