$(function() {
    var preview_canvas = $('#pdf-canvas').get(0),
	preview_canvas_ctx = preview_canvas.getContext('2d');

    function showPDF(pdf_url) {
	PDFJS.getDocument({ url: pdf_url }).then(function(pdf_doc) {
	    var maybeMetadata = pdf_doc.getMetadata().then(function(res) { return res["metadata"] });

	    // Show the first page
	    showPage(pdf_doc, 1);
	}).catch(function(error) {
	    alert(error.message);
	});;
    }

    function showPage(pdf, page_no) {
	// While page is being rendered hide the canvas so that the user knows
	// that something is happening.
	$("#pdf-canvas").hide();

	// Fetch the page
	pdf.getPage(page_no).then(function(page) {
	    // As the canvas is of a fixed width we need
	    // to set the scale of the viewport accordingly
	    var required_scale = preview_canvas.width / page.getViewport(1).width;

	    // Get viewport of the page at required scale
	    var viewport = page.getViewport(required_scale);

	    // Ensure that the canvas is of the same size as the output PDF
	    preview_canvas.height = viewport.height;

	    var renderContext = {
		canvasContext: preview_canvas_ctx,
		viewport: viewport
	    };

	    page.render(renderContext).then($("#pdf-canvas").show());
	});
    }

    $("#uploaded_file").on('change', function() {
	// Naively attempt to determine whether this is a PDF
	if(['application/pdf'].indexOf($("#uploaded_file").get(0).files[0].type) == -1) {
	    alert('Error: Not a PDF');
	    return;
	}

	// Send the object url of the pdf
	showPDF(URL.createObjectURL($("#uploaded_file").get(0).files[0]));
    });
});
