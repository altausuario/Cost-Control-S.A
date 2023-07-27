var input_daterange;
var access_users = {
    list: function (all) {
        var parameters = {
            'action': 'search_report_budget',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        $('#data').DataTable({
            responsive: true,
             scrollX: true,
             autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: parameters,
                dataSrc: "",
            },
             order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
        ],
            initComplete: function (settings, json) {
            }
        });
    },
};
$(function () {
    input_daterange = $('#id_date_range');
    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });
    $('.drp-buttons').hide();
    $('.btnSearch').on('click', function () {
        access_users.list(false);
    });
    $('.btnSearchAll').on('click', function () {
        access_users.list(true);
    });
    access_users.list(false);
});