/* ========================================================================= */
/*	Preloader
/* ========================================================================= */

jQuery(window).load(function(){
   
	$("#preloader").fadeOut("slow");

});

/* ========================================================================= */
/*  Welcome Section Slider
/* ========================================================================= */

$(function() {

    var Page = (function() {

        var $navArrows = $( '#nav-arrows' ),
            $nav = $( '#nav-dots > span' ),
            slitslider = $( '#slider' ).slitslider( {
                onBeforeChange : function( slide, pos ) {

                    $nav.removeClass( 'nav-dot-current' );
                    $nav.eq( pos ).addClass( 'nav-dot-current' );

                }
            } ),

            init = function() {

                initEvents();
                
            },
            initEvents = function() {

                // add navigation events
                $navArrows.children( ':last' ).on( 'click', function() {

                    slitslider.next();
                    return false;

                } );

                $navArrows.children( ':first' ).on( 'click', function() {
                    
                    slitslider.previous();
                    return false;

                } );

                $nav.each( function( i ) {
                
                    $( this ).on( 'click', function( event ) {
                        
                        var $dot = $( this );
                        
                        if( !slitslider.isActive() ) {

                            $nav.removeClass( 'nav-dot-current' );
                            $dot.addClass( 'nav-dot-current' );
                        
                        }
                        
                        slitslider.jump( i + 1 );
                        return false;
                    
                    } );
                    
                } );

            };

            return { init : init };

    })();

    Page.init();

});

var currentTab = 0; // Current tab is set to be the first tab (0) (for multiple forms in one page)

$(document).ready(function(){
	/* ========================================================================= */
	/*	Menu item highlighting
	/* ========================================================================= */

	jQuery('#nav').singlePageNav({
		offset: jQuery('#nav').outerHeight(),
		filter: ':not(.external)',
		speed: 2000,
		currentClass: 'current',
		easing: 'easeInOutExpo',
		updateHash: true,
		beforeStart: function() {
			console.log('begin scrolling');
		},
		onComplete: function() {
			console.log('done scrolling');
		}
	});
	
    $(window).scroll(function () {
        if ($(window).scrollTop() > 400) {
            $(".navbar-brand a").css("color","#fff");
            $("#navigation").removeClass("animated-header");
        } else {
            $(".navbar-brand a").css("color","inherit");
            $("#navigation").addClass("animated-header");
        }
    });
	
	/* ========================================================================= */
	/*	Fix Slider Height
	/* ========================================================================= */	

    // Slider Height
    var slideHeight = $(window).height();
    
    $('#home-slider, #slider, .sl-slider, .sl-content-wrapper').css('height',slideHeight);

    $(window).resize(function(){'use strict',
        $('#home-slider, #slider, .sl-slider, .sl-content-wrapper').css('height',slideHeight);
    });
	
	
	
	$("#works, #testimonial").owlCarousel({	 
		navigation : true,
		pagination : false,
		slideSpeed : 700,
		paginationSpeed : 400,
		singleItem:true,
		navigationText: ["<i class='fa fa-angle-left fa-lg'></i>","<i class='fa fa-angle-right fa-lg'></i>"]
	});
	
	
	/* ========================================================================= */
	/*	Featured Project Lightbox
	/* ========================================================================= */

	$(".fancybox").fancybox({
		padding: 0,

		openEffect : 'elastic',
		openSpeed  : 650,

		closeEffect : 'elastic',
		closeSpeed  : 550,

		closeClick : true,
			
		beforeShow: function () {
			this.title = $(this.element).attr('title');
			this.title = '<h3>' + this.title + '</h3>' + '<p>' + $(this.element).parents('.portfolio-item').find('img').attr('alt') + '</p>';
		},
		
		helpers : {
			title : { 
				type: 'inside' 
			},
			overlay : {
				css : {
					'background' : 'rgba(0,0,0,0.8)'
				}
			}
		}
    });
    showTab(currentTab); // Display the current tab (for multiple forms in one page)

    $('#SaaSBusiness').on('change', function(){
        if (this.value == 'No')
        {
            $("#SchoolDetailss").hide();
        }
        else
        {
            document.getElementById("SaaSSchoolName").required="true";
            document.getElementById("SaaSSchoolWebsite").required="true";
            document.getElementById("SaaSSchoolFB").required="true";
            $("#SchoolDetailss").show();
        }
    });
});


/* ==========  START GOOGLE MAP ========== */

// When the window has finished loading create our google map below
google.maps.event.addDomListener(window, 'load', init);

function init() {
    // Basic options for a simple Google Map
    // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions

	    var myLatLng = new google.maps.LatLng(12.972744, 80.213812);

	    var mapOptions = {
	        zoom: 15,
	        center: myLatLng,
	        disableDefaultUI: true,
	        scrollwheel: false,
	        navigationControl: true,
	        mapTypeControl: false,
	        scaleControl: false,
	        draggable: true,

        // How you would like to style the map. 
        // This is where you would paste any style found on Snazzy Maps.
        styles: [{
            featureType: 'water',
            stylers: [{
                color: '#46bcec'
            }, {
                visibility: 'on'
            }]
        }, {
            featureType: 'landscape',
            stylers: [{
                color: '#f2f2f2'
            }]
        }, {
            featureType: 'road',
            stylers: [{
                saturation: -100
            }, {
                lightness: 45
            }]
        }, {
            featureType: 'road.highway',
            stylers: [{
                visibility: 'simplified'
            }]
        }, {
            featureType: 'road.arterial',
            elementType: 'labels.icon',
            stylers: [{
                visibility: 'off'
            }]
        }, {
            featureType: 'administrative',
            elementType: 'labels.text.fill',
            stylers: [{
                color: '#444444'
            }]
        }, {
            featureType: 'transit',
            stylers: [{
                visibility: 'off'
            }]
        }, {
            featureType: 'poi',
            stylers: [{
                visibility: 'off'
            }]
        }]
    };

    // Get the HTML DOM element that will contain your map 
    // We are using a div with id="map" seen below in the <body>
    var mapElement = document.getElementById('map-canvas');

    // Create the Google Map using our element and options defined above
    var map = new google.maps.Map(mapElement, mapOptions);

    // Let's also add a marker while we're at it
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(12.972744, 80.213812),
        map: map,
    });
}

// ========== END GOOGLE MAP ========== //

var wow = new WOW ({
	offset:       75,          // distance to the element when triggering the animation (default is 0)
	mobile:       false,       // trigger animations on mobile devices (default is true)
});
wow.init();

// ========== Subscribe Email To Google Sheets ========== //

function postEmailToGoogle() {
     
        var email = $('#Email').val();
        if ((email !== "") && (validateEmail(email))) {
            $.ajax({
                url: "https://docs.google.com/forms/d/e/1FAIpQLScuxL8dDHh6mbOznWQ7jYaTn6ar69lQ2ctksVUnC7gEGR74VQ/formResponse",
                data: { "entry.1522510562": email },
                type: "POST",
                dataType: "xml",
                statusCode: {
                    0: function () {
//                        window.location.replace("ThankYou.html");
                        $("#subscribemail")[0].reset();
                        $(subscribed).html('Thank you!');
                        $(subscribed).fadeOut(5000);
                    },
                    200: function () {
//                        window.location.replace("ThankYou.html");
                        $("#subscribemail")[0].reset();
                        $(subscribed).html('Thank you!');
                        $(subscribed).fadeOut(5000);
                    }
                }
            });
        }
        else {
            //error message
            $(subscribed).html('Please enter a valid email address.');   
        }
    }

function validateEmail(email) {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }
// ========== End Subscribe Email To Google Sheets ========== //

// ========== Geekz Application To Google Sheets ========== //

    function postContactToGoogle() {
        var firstname = $('#FirstName').val();
        var lastname = $('#LastName').val();
        var gender = $('#Gender').val();
        var dob = $('#DOB').val();
        var grade = $('#Grade').val();
        var school = $('#RecentSchool').val();
        var fathername = $('#FatherName').val();
        var fatheroccupation = $('#FatherOccupation').val();
        var mothername = $('#MotherName').val();
        var motheroccupation = $('#MotherOccupation').val();
        var income = $('#Income').val();
        var address = $('#Address').val();
        var applicationemail = $('#ApplicationEmail').val();
        var phone = $('#Phone').val();
        var commute = $('#Commute').val();
        var pickup = $('#CommuteLocation').val();
        var proud = $('#Proud').val();
        var familytime = $('#FamilyTime').val();
        var passion = $('#Passion').val();
        var parentalpri = $('#ParentalPriorities').val();
        var health = $('#Health').val();
        var studenthistory = $('#History').val();
        var extra = $('#Extra').val();
        var marketing = $('#Marketing').val();

            $.ajax({
                url: "https://docs.google.com/forms/d/e/1FAIpQLSciq4yYlJRh3mssfqgQSVvoBGAUFTkM8hRmT4XTkyd3QcbnpQ/formResponse",
                data: { "entry.1604377194": firstname, "entry.1940714055": lastname, "entry.98025862": gender, "entry.976596705": dob, "entry.382730210": grade, "entry.523130611": school, "entry.1674665686": fathername, "entry.710713382": fatheroccupation, "entry.352289270": mothername, "entry.807161894": motheroccupation, "entry.2017962840": income, "entry.208625122": address, "entry.951997613": applicationemail, "entry.1308318214": phone, "entry.519255434": commute, "entry.589543065": pickup, "entry.1229821226": proud, "entry.403363822": familytime, "entry.563749857": passion, "entry.426145336": parentalpri, "entry.1121941208": health, "entry.1404358560": studenthistory, "entry.586229829": extra, "entry.1564202305": marketing },
                type: "POST",
                dataType: "xml",
                statusCode: {
                    0: function () {
                        $(applications).fadeOut();
                        $(tips).fadeOut();
                        $(geekzapply).html('Your application’s on its way. Geekz admissions team will be in touch with you shortly. Good luck!');
                    },
                    200: function () {
                        $(applications).fadeOut();
                        $(tips).fadeOut();
                        $(geekzapply).html('Your application’s on its way. Geekz admissions team will be in touch with you shortly. Good luck!');
                    }
                }
            });
    }

// ========== End Geekz Application To Google Sheets ========== //

// ========== Geekz Affiliation To Google Sheets ========== //

    function postAffiliateToGoogle() {
        var iam = $('#IAm').val();
        var loveto = $('#LoveTo').val();
        var city = $('#City').val();
        var academicyear = $('#AcademicYear').val();
        var studio = $('#Studio').val();
        var fullname = $('#FullName').val();
        var occupation = $('#Occupation').val();
        var affiliateemail = $('#AffiliateEmail').val();
        var affiliatephone = $('#AffiliatePhone').val();
        var moreinfo = $('#MoreInfo').val();
        var branding = $('#Branding').val();

            $.ajax({
                url: "https://docs.google.com/forms/d/e/1FAIpQLSeyB1UIK1oCPDPXt-__reZZO3X9VMPAw3X06KYjLaAz1LGS5A/formResponse",
                data: { "entry.1554984773": iam, "entry.2080001749": loveto, "entry.271068763": city, "entry.2128247136": academicyear, "entry.49096205": studio, "entry.1482264808": fullname, "entry.134970049": occupation, "entry.1234350953": affiliatephone, "entry.1602031151": affiliateemail, "entry.721984861": moreinfo, "entry.197306362": branding },
                type: "POST",
                dataType: "xml",
                statusCode: {
                    0: function () {
                        $(signup).fadeOut();
//                        $(tips).fadeOut();
                        $(geekzsignup).html('<br /><br /><br /><br />Your message on its way. Geekz team will be in touch with you shortly. <br />Good luck!');
                        $('html, body').animate({scrollTop: $("#contact").offset().top}, 2000);
                    },
                    200: function () {
                        $(signup).fadeOut();
//                        $(tips).fadeOut();
                        $(geekzsignup).html('<br /><br /><br /><br />Your message on its way. Geekz team will be in touch with you shortly. <br />Good luck!');
                        $('html, body').animate({scrollTop: $("#contact").offset().top}, 2000);
                    }
                }
            });
    }

// ========== End Geekz Affiliation To Google Sheets ========== //

// ========== Geekz Homeschool Application To Google Sheets ========== //

    function postHomeschoolToGoogle() {
        var homefullname = $('#HSFullName').val();
        var homedob = $('#HSDOB').val();
        var homegrade = $('#HSGrade').val();
        var homeparentname = $('#HSParentName').val();
        var homeoccupation = $('#HSOccupation').val();
        var homefb = $('#HSFB').val();
        var homeemail = $('#HSEmail').val();
        var homephone = $('#HSPhone').val();
        var homebranding = $('#HSBranding').val();
        var homeaddress = $('#HSAddress').val();
        
            $.ajax({
                url: "https://docs.google.com/forms/d/e/1FAIpQLSe4MfZM4pUHcBLyId68NmFB3SsFpjvBMFTg_Zlt7PsPHNZdaA/formResponse",
                data: { "entry.1884265043": homefullname, "entry.235218874": homedob, "entry.1409244820": homegrade, "entry.404257411": homeparentname, "entry.1746769121": homeoccupation, "entry.218925378": homefb, "entry.2051454829": homeemail, "entry.1525402407": homephone, "entry.562565552": homebranding, "entry.1441468082": homeaddress },
                type: "POST",
                dataType: "xml",
                statusCode: {
                    0: function () {
                        $(homeschool).fadeOut();
//                        $(tips).fadeOut();
                        $(geekzhomeschool).html('<br /><br /><br /><br />Your message on its way. Geekz team will be in touch with you shortly. <br />Good luck!');
                        $('html, body').animate({scrollTop: $("#contact").offset().top}, 2000);
                    },
                    200: function () {
                        $(homeschool).fadeOut();
//                        $(tips).fadeOut();
                        $(geekzhomeschool).html('<br /><br /><br /><br />Your message on its way. Geekz team will be in touch with you shortly. <br />Good luck!');
                        $('html, body').animate({scrollTop: $("#contact").offset().top}, 2000);
                    }
                }
            });
    }

// ========== End Geekz Homeschool Application To Google Sheets ========== //


// ========== Geekz Inquiry To Google Sheets ========== //

    function postInquiryToGoogle() {
        var inquiryname = $('#InquiryName').val();
        var inquirydob = $('#InquiryDOB').val();
        var inquirygrade = $('#InquiryGrade').val();
        var inquiryemail = $('#InquiryEmail').val();
        var inquiryphone = $('#InquiryPhone').val();
        var inquirysubject = $('#InquirySubject').val();
        var inquirymessage = $('#InquiryMessage').val();
        var inquirymarketing = $('#InquiryMarketing').val();

            $.ajax({
                url: "https://docs.google.com/forms/d/e/1FAIpQLSf0rhz1oD1BTy_5K0ErLpjw0L5g7ZoOvwX4pH6kvystdQ4TPg/formResponse",
                data: { "entry.1554984773": inquiryname, "entry.2080001749": inquirydob, "entry.271068763": inquirygrade, "entry.2128247136": inquiryemail, "entry.1234350953": inquiryphone, "entry.1602031151": inquirysubject, "entry.721984861": inquirymessage, "entry.197306362": inquirymarketing },
                type: "POST",
                dataType: "xml",
                statusCode: {
                    0: function () {
                        $(inquiry).fadeOut();
//                        $(tips).fadeOut();
                        $(geekzinquiry).html('<br /><br /><br /><br />Your message on its way. Geekz support team will be in touch with you shortly. <br />Good luck!');
                        $('html, body').animate({scrollTop: $("#contact").offset().top}, 2000);
                    },
                    200: function () {
                        $(inquiry).fadeOut();
//                        $(tips).fadeOut();
                        $(geekzinquiry).html('<br /><br /><br /><br />Your message on its way. Geekz support team will be in touch with you shortly. <br />Good luck!');
                        $('html, body').animate({scrollTop: $("#contact").offset().top}, 2000);
                    }
                }
            });
    }

// ========== End Geekz Inquiry To Google Sheets ========== //

//===========Day At Geekz Video =====================//

var dayAtGeekzBtn = document.getElementById("dayAtGeekz");
var modal = document.getElementById("myModal");
var closeBtn = document.getElementsByClassName("close")[0];
var video = document.getElementById("myVideo");

dayAtGeekzBtn.onclick = function(){
    modal.style.display = "block";
}


closeBtn.onclick = function(){
    video.pause();
    video.currentTime = 0;
    modal.style.display = "none";
}



window.onclick = function(event) {
    if (event.target == modal) {
        video.pause();
        video.currentTime = 0;
        modal.style.display = "none";
    }
}


//Start Script for Geekz Saas-Become A Microschool application-multi step forms

function showTab(n) {
    // This function will display the specified tab of the form...
    var x = document.getElementsByClassName("tabb");
    x[n].style.display = "block";
    //... and fix the Previous/Next buttons:
    if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
    } else {
    document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
    } else {
    document.getElementById("nextBtn").innerHTML = "Next";
    }
    //... and run a function that will display the correct step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("tabb");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // if you have reached the end of the form...
    if (currentTab >= x.length) {
    // ... the form gets submitted:
    document.getElementById("SaaSApplication").submit();
    return false;
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var x, y, z, i, valid = true;
    x = document.getElementsByClassName("tabb");
    y = x[currentTab].getElementsByTagName("input");
    z = x[currentTab].getElementsByTagName("select");
    ta = x[currentTab].getElementsByTagName("textarea");
    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
        //validation for 3 fields on the basis of dropdown
        if (y[i].id == "SaaSSchoolName" || y[i].id == "SaaSSchoolWebsite" || y[i].id == "SaaSSchoolFB") 
        {
            if (y[i].required)
            {
                if (y[i].value == "") 
                {
                    // add an "invalid" class to the field:
                    y[i].className += " invalid";
                    if(y[i].id=="SaaSSchoolName"){
                        $("#errmsgsn").show();
                    }
                    if(y[i].id=="SaaSSchoolWebsite"){
                        $("#errmsgsw").show();
                    }
                    if(y[i].id=="SaaSSchoolFB"){
                        $("#errmsgsfb").show();
                    }
                    // and set the current valid status to false
                    valid = false;
                    continue;
                }
            }
            else
            {
                y[i].className += " invalid";
                if(y[i].id=="SaaSSchoolName"){
                    $("#errmsgsn").hide();
                }
                if(y[i].id=="SaaSSchoolWebsite"){
                    $("#errmsgsw").hide();
                }
                if(y[i].id=="SaaSSchoolFB"){
                    $("#errmsgsfb").hide();
                }
                continue;
            }
        }
        // If a field is empty...
        if (y[i].value == "") 
        {
            // add an "invalid" class to the field:
            y[i].className += " invalid";
            //check all the id one by one if any field is empty then show the error msg below field
            if(y[i].id=="SaaSDOB"){
                $("#errmsgdob").show();
            }
            if(y[i].id=="SaaSPhone"){
                $("#errmsgph").show();
            }
            if(y[i].id=="SaaSSchoolArea"){
                $("#errmsgsa").show();
            }
            if(y[i].id=="SaaSSchoolCity"){
                $("#errmsgsc").show();
            }
            if(y[i].id=="SaaSLinkedin"){
                $("#errmsgslin").show();
            }
            if(y[i].id=="SaaSOccupation"){
                $("#errmsgocc").show();
            }
            
            
            /*y[i].validationMessage;
            alert(y[i].validationMessage);*/
            /*alert(y[i].setCustomValidity("Please fill out this field."));
            y[i].setCustomValidity("Please fill out this field.");*/
            // and set the current valid status to false
            valid = false;
        }
        else
        {
            if(y[i].id=="SaaSDOB"){
                $("#errmsgdob").hide();
            }
            if(y[i].id=="SaaSPhone"){
                $("#errmsgph").hide();
            }
            if(y[i].id=="SaaSLTB"){
                $("#errmsgltb").hide();
            }
            if(y[i].id=="SaaSSchoolArea"){
                $("#errmsgsa").hide();
            }
            if(y[i].id=="SaaSSchoolCity"){
                $("#errmsgsc").hide();
            }
            if(y[i].id=="SaaSLinkedin"){
                $("#errmsgslin").hide();
            }
            if(y[i].id=="SaaSOccupation"){
                $("#errmsgocc").hide();
            }
        }
    }
    for (i = 0; i < z.length; i++) {
        // If a field is empty...
        if (z[i].value == "") {
            // add an "invalid" class to the field:
            z[i].className += " invalid";
            if(z[i].id=="SaaSLTB"){
                $("#errmsgltb").show();
            }
            if(z[i].id=="SaaSSchoolMode"){
                $("#errmsgsm").show();
            }
            if(z[i].id=="SaaSSOperate"){
                $("#errmsgop").show();
            }
            if(z[i].id=="SaaSBusiness"){
                $("#errmsgbus").show();
            }
            // and set the current valid status to false
            valid = false;
        }
        else{
            if(z[i].id=="SaaSLTB"){
                $("#errmsgltb").hide();
            }
            if(z[i].id=="SaaSSchoolMode"){
                $("#errmsgsm").hide();
            }
            if(z[i].id=="SaaSSOperate"){
                $("#errmsgop").hide();
            }
            if(z[i].id=="SaaSBusiness"){
                $("#errmsgbus").hide();
            }
        }
    }
    for (i = 0; i < ta.length; i++) {
        // If a field is empty...
        if (ta[i].value == "") {
            // add an "invalid" class to the field:
            ta[i].className += " invalid";
            if(ta[i].id=="SaaSPassion"){
                $("#errmsgpass").show();
            }
            if(ta[i].id=="SaaSWhyAffiliate"){
                $("#errmsgwaff").show();
            }
            // and set the current valid status to false
            valid = false;
        }
        else{
            if(ta[i].id=="SaaSPassion"){
                $("#errmsgpass").hide();
            }
            if(ta[i].id=="SaaSWhyAffiliate"){
                $("#errmsgwaff").hide();
            }
        }
    }
    // If the valid status is true, mark the step as finished and valid:
    if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class on the current step:
    x[n].className += " active";
}
//end Script for swiping multiple forms 

