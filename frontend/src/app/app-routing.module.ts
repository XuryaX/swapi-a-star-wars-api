import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DatasetListComponent } from './dataset-list/dataset-list.component';
import { DatasetDetailsComponent } from './dataset-details/dataset-details.component';

const routes: Routes = [
  { path: '', component: DatasetListComponent },
  { path: 'dataset/:id', component: DatasetDetailsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
