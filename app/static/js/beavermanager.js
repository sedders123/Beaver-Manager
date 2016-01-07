jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.document.location = $(this).data("href");
    });
});

$(document).ready(function() {
	$(chart_id).highcharts({
		chart: chart,
		title: title,
		series: series,
    plotOptions: plotOptions
	});
});
