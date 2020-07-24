import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material';

@Component({
  selector: 'app-are-you-sure-dialog',
  templateUrl: './are-you-sure-dialog.component.html',
  styleUrls: ['./are-you-sure-dialog.component.scss']
})
export class AreYouSureDialogComponent implements OnInit {

  public static result = false;
  constructor( public thisDialogRef: MatDialogRef<AreYouSureDialogComponent>) {
  }

  ngOnInit() {
  }

  onYes(): void {
    AreYouSureDialogComponent.result = true;
    this.onClose();
  }

  onNo(): void {
    AreYouSureDialogComponent.result = false;
    this.onClose();
  }

  onClose(): void {
    this.thisDialogRef.close();
  }
}
