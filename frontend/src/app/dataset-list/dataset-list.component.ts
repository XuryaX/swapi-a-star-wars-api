import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from './../../environments/environment';

@Component({
  selector: 'app-dataset-list',
  templateUrl: './dataset-list.component.html',
  styleUrls: ['./dataset-list.component.css']
})
export class DatasetListComponent implements OnInit {
  datasets: any[] = [];
  serverUrl = environment.serverUrl;

  constructor(private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
    this.fetchDatasets();
  }

  fetchDatasets(): void {
    this.http.get<any[]>(`${this.serverUrl}/api/metadata/list`).subscribe(
      data => {
        this.datasets = data;
      },
      error => {
        console.error('Error fetching datasets:', error);
      }
    );
  }

  openDataset(datasetId: string): void {
    this.router.navigate(['/dataset', datasetId]);
  }
}
