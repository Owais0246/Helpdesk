$(document).ready(function () {
  $("#tickets-table").DataTable({
    language: {
      paginate: {
        previous: "<i class='mdi mdi-chevron-left'>",
        next: "<i class='mdi mdi-chevron-right'>",
      },
    },
    drawCallback: function () {
      $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
    },
  }),
    $(".dataTables_length select").addClass("form-select form-select-sm"),
    $(".dataTables_length select").removeClass(
      "custom-select custom-select-sm"
    ),
    $(".dataTables_length label").addClass("form-label");
});
