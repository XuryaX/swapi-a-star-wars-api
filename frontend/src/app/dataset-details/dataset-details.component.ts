import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

import { environment } from './../../environments/environment';


@Component({
  selector: 'app-dataset-details',
  templateUrl: './dataset-details.component.html',
  styleUrls: ['./dataset-details.component.css']
})
export class DatasetDetailsComponent implements OnInit {
  datasetId: string = '';
  serverUrl = environment.serverUrl;
  data: any[] = [];
  columns: string[] = [];
  selectedColumns: string[] = [];
  pageNumber: number = 1;
  hasMore: boolean = true;

  constructor(private route: ActivatedRoute, private http: HttpClient) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.datasetId = params['id'];
      this.loadData();
    });
  }

  loadData(): void {
    this.http.get<any[]>(`${this.serverUrl}/data/${this.datasetId}/${this.pageNumber}`).subscribe(
      data => {
        if (data.length === 0) {
          this.hasMore = false;
        } else {
          this.data.push(...data);
          if (this.columns.length === 0) {
            this.columns = Object.keys(data[0]);
          }
        }
      },
      error => {
        console.error('Error fetching dataset details:', error);
      }
    );
  }

  loadMoreData(): void {
    this.pageNumber++;
    this.loadData();
  }

  applyColumnSelection(): void {
    const columns = this.selectedColumns.join(',');
    this.http.get<any>(`${this.serverUrl}/api/data/value_count/${this.datasetId}/${columns}`).subscribe(
      response => {
        this.data = response.data;
        this.hasMore = false;
      },
      error => {
        console.error('Error fetching value counts:', error);
      }
    );
  }

  reset(): void {
    this.hasMore = true;
    this.pageNumber = 1;
    this.data = [];
    this.loadData();
  }
}
