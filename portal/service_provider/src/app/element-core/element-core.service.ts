import { AUTHGWCONSTANTS } from './../authorization/authconstants';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable()
export class ElementCoreService {

  public static dialogResult = false;
  headers: any;
  httpClient: any;

  constructor(private http: HttpClient) {
    const token = localStorage.getItem(AUTHGWCONSTANTS.bearerToken);
    const xOriginKey = localStorage.getItem(AUTHGWCONSTANTS.xOriginKey);
    const xApiKey = localStorage.getItem(AUTHGWCONSTANTS.xApiKey);
    this.headers = {
      // Authorization: 'Bearer ' + token,
      'x-Origin-Key': 'gAAAAABdLWqL32l75L4G2CH_ftHkes0ObTkOQ2jlKzg_shxL47r6sCFA2fZJ_NUtnkzbmzUL-CiAkEcJIwp7QuBOewwy65Tsnk8SXFyFTJ-2iSv_11G635A='
    //   'x-Api-Key': xApiKey
    };
  }

  getAdminInfo(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl + '/web/profile', {
      headers: this.headers
    });
  }
  editDriver(body): Observable<any> {
    return this.http.put<any>(environment.proxyApiUrl + '/api/drivers', body, {
      headers: this.headers
    });
  }

  uploadFile(body): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl + '/api/upload_image', body, {
      headers: this.headers
    });
  }

  getProfileInfo(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl + '/web/profile', {
      headers: this.headers
    });
  }
}
