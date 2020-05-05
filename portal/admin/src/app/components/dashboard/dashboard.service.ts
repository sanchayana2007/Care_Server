import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AUTHGWCONSTANTS } from '../../authorization/authconstants';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  public static dialogResult = false;
  headers: any;
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

  getDashBoardReport(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl + '/report/dashboard', {
      headers: this.headers
    });
  }
}

