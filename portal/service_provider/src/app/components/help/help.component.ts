import { ElementCoreService } from './../../element-core/element-core.service';
import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA,
  MatSnackBarConfig, MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-help',
  templateUrl: './help.component.html',
  styleUrls: ['./help.component.scss'],
  providers: [ElementCoreService]
})
export class HelpComponent implements OnInit {

  constructor(public thisDialogRef: MatDialogRef<HelpComponent>,
    @Inject(MAT_DIALOG_DATA) private dailogData: any,
    private snackBar: MatSnackBar, private service: ElementCoreService) { }

  ngOnInit() {
  }

  onClose(): void {
    this.thisDialogRef.close();
  }

}
