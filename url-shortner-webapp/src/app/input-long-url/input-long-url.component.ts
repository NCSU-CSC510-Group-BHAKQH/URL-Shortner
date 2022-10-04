import { Component, Inject, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import { MatDialog, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from '../api.service';
import { URL } from '../models/URL'

export interface DialogData {
  title: string;
  content: string;
}

@Component({
  selector: 'app-input-long-url',
  templateUrl: './input-long-url.component.html',
  styleUrls: ['./input-long-url.component.scss']
})
export class InputLongUrlComponent implements OnInit {
  
  // variables for form and Regex
  urlShortnerForm : FormGroup;
  urlRegex = new RegExp('(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[/\\w .-]*/?');
  loading: boolean = false;
  
  constructor(private fb: FormBuilder, private _apiService: ApiService, public dialog: MatDialog) {
    // initialize the form and setup validators for form fields
    this.urlShortnerForm = this.fb.group({
    long_url: ['', [Validators.required, Validators.pattern(this.urlRegex) ]]
 });}

 // submit function to call actual API and get short URL
  getShortURL(){
    // only call API if form is valid
    if(this.urlShortnerForm.valid)
    {
      this.urlShortnerForm.markAllAsTouched();
      this.loading = true;
      const newURL = new URL({
        "long_url": this.urlShortnerForm.get('long_url')
      });

      this._apiService.addURL(newURL).subscribe(
        (data) => {
          console.log(data);
          this.loading = false;
          const dialogRef = this.dialog.open(DialogShortUrl, {
            data: {
              title: 'Short URL Generated',
              content: 'Short URL is: ' + data.stub
            },
          });

          dialogRef.afterClosed().subscribe(result => {
            location.reload();
          });
        },
        (err) => {
          console.log(err);
          this.loading = false;
          this.dialog.open(DialogShortUrl, {
            data: {
              title: 'Error Occurred',
              content: err.message
            },
          });
        }
      );
      console.log(this.urlShortnerForm.value);
    }
  }

  ngOnInit(): void {
  }

}

@Component({
  selector: 'dialog-short-url',
  templateUrl: 'dialog-short-url.html',
})
export class DialogShortUrl {
  constructor(@Inject(MAT_DIALOG_DATA) public data: DialogData) {}

  content: string = this.data.content
  title: string = this.data.title
}
