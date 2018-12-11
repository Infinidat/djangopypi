/* This js file assits with styling datatables by adding
 * glyph elements to the search box, the sorted columns and
 * the pagination controls, which is not possible using css alone */

$(document).on('init.dt', function(e, settings) {
    $(e.target).append($("<span/>").addClass("glyphicon glyphicon-search form-control-feedback"));
});

$(document).on('order.dt', function(e, settings) {
    $("i", $(".sorting, .sorting_asc, .sorting_desc", e.target)).remove();
    $(".sorting_asc", e.target).append($("<i/>").addClass("glyphicon glyphicon-chevron-up"));
    $(".sorting_desc", e.target).append($("<i/>").addClass("glyphicon glyphicon-chevron-down"));
});

$(document).on('draw.dt', function(e, settings) {
    $(".previous", $(e.target).parent()).html($("<i/>").addClass("glyphicon glyphicon-backward"));
    $(".next", $(e.target).parent()).html($("<i/>").addClass("glyphicon glyphicon-forward"));
});
