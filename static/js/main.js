/* ========================================================================= */
/*	Preloader
/* ========================================================================= */

jQuery(window).load(function(){
   
	$("#preloader").fadeOut("slow");

});

//=======School Branch Slideshow - Declaring the global variable array ========//
var slideIndex = new Array(2);
slideIndex[0]=1;
slideIndex[1]=1;
//alert('global variable initialized');

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

	jQuery('#nav1, #nav2').singlePageNav({
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
            document.getElementById("SaaSSchoolName").removeAttribute("required");
            document.getElementById("SaaSSchoolWebsite").removeAttribute("required");
            document.getElementById("SaaSSchoolFB").removeAttribute("required");
        }
        else
        {
            document.getElementById("SaaSSchoolName").required="true";
            document.getElementById("SaaSSchoolWebsite").required="true";
            document.getElementById("SaaSSchoolFB").required="true";
            $("#SchoolDetailss").show();
        }
    });
    window.onload(checkfinancialvalue())
    var m;
    var slideshows = document.getElementsByClassName("affiliatesSlideshowContainer"); 
    alert('no of slideshows' + slideshows.length);
    for(m=0; m < slideshows.length;  m++){
         showSlides(1,m);
    }    
    

});

var wow = new WOW ({
	offset:       75,          // distance to the element when triggering the animation (default is 0)
	mobile:       false,       // trigger animations on mobile devices (default is true)
});



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
                        $(geekzapply).html('Your application’s on its wayy. Geekz admissions team will be in touch with you shortly. Good luck!');
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
    try{
        document.getElementById("SaaSApplication").submit();
    }
    catch(err){

    }
    try{
        document.getElementById("SaaSAudition").submit();
        thankyoumsg();
    }
    catch(err){
        
    }
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
        if (y[i].id == "SaaSSchoolName" || y[i].id == "SaaSSchoolWebsite" || y[i].id == "SaaSSchoolFB" || y[i].id == "SaaSFromWhere") 
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
                    if(y[i].id=="SaaSFromWhere"){
                        $("#errmsgfromwhere").show();
                    }
                    // and set the current valid status to false
                    valid = false;
                    continue;
                }
                else
                {
                    y[i].className += " valid";
                    if(y[i].id=="SaaSSchoolName"){
                        $("#errmsgsn").hide();
                    }
                    if(y[i].id=="SaaSSchoolWebsite"){
                        $("#errmsgsw").hide();
                    }
                    if(y[i].id=="SaaSSchoolFB"){
                        $("#errmsgsfb").hide();
                        if(isValidURL(y[i].value)){
                            $("#errmsgvalsfb").hide();
                        }else{
                            $("#errmsgvalsfb").show();
                            valid = false;
                        }
                    }
                    if(y[i].id=="SaaSFromWhere"){
                        $("#errmsgfromwhere").hide();
                    }
                    continue; 
                }
            }
            else
            {
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
            if(y[i].id=="SaaSYoutubeLink"){
                $("#errmsgytubelink").show();
            }
            if(y[i].id=="SaaSNoOfStu"){
                if(isNaN(y[i].value)){
                    //if not a number or length is not equal to 10
                    $("#errmsgvalnoofstudent").show()
                }else{
                $("#errmsgnoofstudent").show();
                }
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
            y[i].className += " valid";
            if(y[i].id=="SaaSDOB"){
                $("#errmsgdob").hide();
            }
            if(y[i].id=="SaaSPhone"){
                $("#errmsgph").hide();
                if( (isNaN(y[i].value)) || (y[i].value.length!=10) ){
                    //if not a number or length is not equal to 10
                    $("#errmsgvalph").show()
                    valid = false;
                }else{
                    $("#errmsgvalph").hide()
                }
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
                if(isValidURL(y[i].value)){
                    $("#errmsgvalslin").hide();
                }else{
                    $("#errmsgvalslin").show();
                    valid = false;
                }
            }
            if(y[i].id=="SaaSOccupation"){
                $("#errmsgocc").hide();
            }
            if(y[i].id=="SaaSYoutubeLink"){
                $("#errmsgytubelink").hide();
                if(isValidURL(y[i].value)){
                    $("#errmsgvalytubelink").hide();
                }else{
                    $("#errmsgvalytubelink").show();
                    valid = false;
                }
            }
            if(y[i].id=="SaaSNoOfStu"){
                $("#errmsgnoofstudent").hide();
                if(isNaN(y[i].value)){
                    //if not a number or length is not equal to 10
                    $("#errmsgvalnoofstudent").show()
                    valid = false;
                }else{
                    $("#errmsgvalnoofstudent").hide()
                }
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
            if(z[i].id=="SaaSESF"){
                $("#errmsgesf").show();
            }
            if(z[i].id=="SaaSCodingSkill"){
                $("#errmsgcodskill").show();
            }
            if(z[i].id=="SaaSPhotoSkill"){
                $("#errmsgphotoskill").show();
            }
            if(z[i].id=="SaaSVideoSkill"){
                $("#errmsgvideoskill").show();
            }
            if(z[i].id=="SaaSPassionToLearn"){
                $("#errmsgpassiontolearn").show();
            }
            if(z[i].id=="SaaSHDWC"){
                $("#errmsghdwc").show();
            }
            if(z[i].id=="SaaSModeInternet"){
                $("#errmsgmodeinternet").show();
            }
            if(z[i].id=="SaaSSpeed"){
                $("#errmsgintspeed").show();
            }
            // and set the current valid status to false
            valid = false;
        }
        else{
            z[i].className += " valid";
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
            if(z[i].id=="SaaSESF"){
                $("#errmsgesf").hide();
            }
            if(z[i].id=="SaaSCodingSkill"){
                $("#errmsgcodskill").hide();
            }
            if(z[i].id=="SaaSPhotoSkill"){
                $("#errmsgphotoskill").hide();
            }
            if(z[i].id=="SaaSVideoSkill"){
                $("#errmsgvideoskill").hide();
            }
            if(z[i].id=="SaaSPassionToLearn"){
                $("#errmsgpassiontolearn").hide();
            }
            if(z[i].id=="SaaSHDWC"){
                $("#errmsghdwc").hide();
            }
            if(z[i].id=="SaaSModeInternet"){
                $("#errmsgmodeinternet").hide();
            }
            if(z[i].id=="SaaSSpeed"){
                $("#errmsgintspeed").hide();
            }
        }
    }
    for (i = 0; i < ta.length; i++) {
        if (ta[i].id == "SaaSFinancial") 
        {
            if (ta[i].required)
            {
                if (ta[i].value == "") 
                {
                    // add an "invalid" class to the field:
                    ta[i].className += " invalid";
                    if(ta[i].id=="SaaSFinancial"){
                        $("#errmsgfinancialmoney").show();
                    }
                    // and set the current valid status to false
                    valid = false;
                    continue;
                }
                else
                {
                    ta[i].className += " valid";
                    if(ta[i].id=="SaaSFinancial"){
                        $("#errmsgfinancialmoney").hide();
                    }
                    continue; 
                }
            }
            else
            {
                continue;
            }
        }
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
            if(ta[i].id=="SaaSQuestions"){
                $("#errmsgquestions").show();
            }
            // and set the current valid status to false
            valid = false;
        }
        else{
            ta[i].className += " valid";
            if(ta[i].id=="SaaSPassion"){
                $("#errmsgpass").hide();
            }
            if(ta[i].id=="SaaSWhyAffiliate"){
                $("#errmsgwaff").hide();
            }
            if(ta[i].id=="SaaSQuestions"){
                $("#errmsgquestions").hide();
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

//to check if a URL is valid or not
function isValidURL(url){
    var urlPattern = "(https?|ftp)://(www\\.)?(((([a-zA-Z0-9.-]+\\.){1,}[a-zA-Z]{2,4}|localhost))|((\\d{1,3}\\.){3}(\\d{1,3})))(:(\\d+))?(/([a-zA-Z0-9-._~!$&'()*+,;=:@/]|%[0-9A-F]{2})*)?(\\?([a-zA-Z0-9-._~!$&'()*+,;=:/?@]|%[0-9A-F]{2})*)?(#([a-zA-Z0-9._-]|%[0-9A-F]{2})*)?";
    urlPattern = "^" + urlPattern + "$";
    var regex = new RegExp(urlPattern);
    return regex.test(url);
}

//check financial value to show financial field
function checkfinancialvalue(){
    var fvalue=document.getElementById("financialvalue");
    var showfinfo=document.getElementById("showfinancialinfo");
    var fmoney=document.getElementById("SaaSFinancial");
    var fromwhere=document.getElementById("SaaSFromWhere");
    var showfstep=document.getElementById("showfinancialinfostep");
    if(fvalue.value=="yes"){
        showfinfo.style['display']='';
        showfinfo.className+="tabb";
        showfstep.style['display']='';
        showfstep.className+="step";
        fmoney.required="true";
        fromwhere.required="true";
    }
}


//thankyou message after audition submission
function thankyoumsg(){
    var showtymsg=document.getElementById('thankyoumsg');
    showtymsg.style['display']='block';
    document.getElementById('prevBtn').style['display']='none';
    document.getElementById('nextBtn').style['display']='none';
    document.getElementById('stepsofform').style['display']='none';
}

//google places api js
var searchInput = 'search_input';

$(document).ready(function () {
    var autocomplete;
    autocomplete = new google.maps.places.Autocomplete((document.getElementById(searchInput)), {
        types: ['geocode'],
    });
	
    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        var near_place = autocomplete.getPlace();
        document.getElementById('loc_lat').value = near_place.geometry.location.lat();
        document.getElementById('loc_long').value = near_place.geometry.location.lng();
		
        document.getElementById('latitude_view').innerHTML = near_place.geometry.location.lat();
        document.getElementById('longitude_view').innerHTML = near_place.geometry.location.lng();
    });
});
$(document).on('change', '#'+searchInput, function () {
    document.getElementById('latitude_input').value = '';
    document.getElementById('longitude_input').value = '';
	
    document.getElementById('latitude_view').innerHTML = '';
    document.getElementById('longitude_view').innerHTML = '';
});


//////////inquiry dropdown validation //////////////

function Validate() {
    var ddlFruits = document.getElementById("HSGrade");
    var ddlFruits1 = document.getElementById("HSBranding");
    var HSPhoneid = document.getElementById("HSPhone");
   
    if (ddlFruits.value == "Enrolling Grade...") {
        //If the "Please Select" option is selected display error.
        document.getElementById("errmsgltb").style.display = "block";
        return false;
    }
    if (ddlFruits1.value == "How Did You Hear About Geekz...") {
        //If the "Please Select" option is selected display error.
        document.getElementById("errmsgltb1").style.display = "block";
        return false;
    } 
    if(isNaN(HSPhoneid.value) || HSPhoneid.value.length!=10){
        document.getElementById("errmsgvalph").style.display = "block";
        return false;
    }
    
    
    return true;
}
function funcURL(){
var schoolname = document.getElementById("schoolname");
var locality   = document.getElementById("locality");
if(schoolname.value!='' && locality.value!=''){
    var sname= schoolname.value;
    var local = locality.value;
    var urll = "Your url is : geekz.school/schoolasaservice/"+sname+local;

    alert(urll);
}
}
//////////// IMAGE TYpEVALIDATION///////
function vv() {
    var x,y;
    y= document.getElementsByTagName("input");
    var allowedExtensions =  
              /(\.jpg|\.jpeg|\.png|\.gif)$/i; 
    for (k = 0; k< y.length; k++) {
      if (y[k].id == "file"||y[k].id == "file2"||y[k].id == "file3"||y[k].id == "file4"){
        var filePath = y[k].value; 
        if ((!allowedExtensions.exec(filePath)) && (filePath != '' ) ) { 
          if(y[k].id == "file"){
            $("#errmsg").show();
            y[k].value = ''; 
          }
          if(y[k].id == "file2"){
            $("#errmsg2").show();
            y[k].value = ''; 
          }
          if(y[k].id == "file3"){
            $("#errmsg3").show();
            y[k].value = ''; 
          }
          if(y[k].id == "file4"){
            $("#errmsg4").show();
            y[k].value = ''; 
          }
        }
      }
     if(y[k].id=="phone"){
        
        if(isNaN(y[k].value)  || y[k].value.length!=10 ){
            //if not a number or length is not equal to 10
            $("#errmsgvalph").show()
            valid = false;
        }else{
            $("#errmsgvalph").hide()
        }
    }
      if( y[k].id=="phone1"){
        
        if( isNaN(y[k].value) || (y[k].value.length!=10) ){
            //if not a number or length is not equal to 10
            $("#errmsgvalph1").show()
            valid = false;
        }
        else{
            $("#errmsgvalph1").hide()
        }
    }
    
    
    
}
}



      
      /*if(y[k].type == "checkbox"){
        if(y[k].id == "c1")
        {
          var ch =  document.getElementById('is_Spacious_Studio').value;
          if (ch =="N"){
            document.getElementById('is_Spacious_Studio').value = 'Y';
          }
          else if (ch=='Y'){
            document.getElementById('is_Spacious_Studio').value = 'N';
          }
        }
        if(y[k].id == "c2")
        {
          var ch1 = document.getElementById('is_Outdoor_PlayLawn').value;
          if (ch1 =="N"){
            document.getElementById('is_Outdoor_PlayLawn').value="Y";
              }
          else if (ch1=='Y'){
            document.getElementById('is_Outdoor_PlayLawn').value= 'N';
            }  
        }
        if(y[k].name == "Commute")
        {
          var ch2 = document.getElementById('is_Commute').value;
          if (ch2 =="N"){
            document.getElementById('is_Commute').value="Y";
              }
          else if (ch2=='Y'){
            document.getElementById('is_Commute').value= 'N';
            }   
        }
        if(y[k].name == "WiFi")
        {
          var ch3 = document.getElementById('is_WiFi').value;
          if (ch3 =="N"){
            document.getElementById('is_WiFi').value="Y";
              }
          else if (ch3=='Y'){
            document.getElementById('is_WiFi').value= 'N';
            }  
        }
        if(y[k].name == "CCTV")
        {
          var ch6 = document.getElementById('is_CCTV').value;
          if (ch6 =="N"){
            document.getElementById('is_CCTV').value="Y";
              }
          else if (ch6=='Y'){
            document.getElementById('is_CCTV').value= 'N';
            }  
        }
        if(y[k].name == "Device")
        {
          var ch4 = document.getElementById('is_Device').value;
          if (ch4 =="N"){
            document.getElementById('is_Device').value="Y";
              }
          else if (ch4=='Y'){
            document.getElementById('is_Device').value= 'N';
            }   
        }
        if(y[k].name == "Food")
        {
          var ch5 = document.getElementById('is_Food').value;
          if (ch5 =="N"){
            document.getElementById('is_Food').value="Y";
              }
          else if (ch5=='Y'){
            document.getElementById('is_Food').value= 'N';
            } 
        }
        if(y[k].name == "After_School")
        {
          var ch8 = document.getElementById('is_After_School').value;
          if (ch8 =="N"){
            document.getElementById('is_After_School').value="Y";
              }
          else if (ch8=='Y'){
            document.getElementById('is_After_School').value= 'N';
            }    
        }
        if(y[k].name == "Residential")
        {
          var ch9 = document.getElementById('is_Residential').value;
          if (ch9 =="N"){
            document.getElementById('is_Residential').value="Y";
              }
          else if (ch9 =='Y'){
            document.getElementById('is_Residential').value= 'N';
            }  
        }
        if(y[k].name == "Daycare")
        {
          var ch7 = document.getElementById('is_Daycare').value;
          if (ch7 =="N"){
            document.getElementById('is_Daycare').value="Y";
              }
          else if (ch7=='Y'){
            document.getElementById('is_Daycare').value= 'N';
            }    
        }

      }*/
   
   

  function showAdd(){
                              
    var ch =  document.getElementById('is_Spacious_Studio').value;
      if (ch =="N"){
        document.getElementById('is_Spacious_Studio').value = 'Y';
      }
      else if (ch=='Y'){
        document.getElementById('is_Spacious_Studio').value = 'N';
      }

}
function showAdd1(){
var ch1 = document.getElementById('is_Outdoor_PlayLawn').value;
if (ch1 =="N"){
  document.getElementById('is_Outdoor_PlayLawn').value="Y";
   }
else if (ch1=='Y'){
  document.getElementById('is_Outdoor_PlayLawn').value= 'N';
 }              
}
function showAdd2(){
var ch2 = document.getElementById('is_Commute').value;
if (ch2 =="N"){
  document.getElementById('is_Commute').value="Y";
   }
else if (ch2=='Y'){
  document.getElementById('is_Commute').value= 'N';
 }                   
}
function showAdd4(){
var ch3 = document.getElementById('is_WiFi').value;
if (ch3 =="N"){
  document.getElementById('is_WiFi').value="Y";
   }
else if (ch3=='Y'){
  document.getElementById('is_WiFi').value= 'N';
 }           
}
function showAdd5(){
var ch4 = document.getElementById('is_Device').value;
if (ch4 =="N"){
  document.getElementById('is_Device').value="Y";
   }
else if (ch4=='Y'){
  document.getElementById('is_Device').value= 'N';
 }          
}
function showAdd6(){
var ch5 = document.getElementById('is_Food').value;
if (ch5 =="N"){
  document.getElementById('is_Food').value="Y";
   }
else if (ch5=='Y'){
  document.getElementById('is_Food').value= 'N';
 }        
}
function showAdd3(){
var ch6 = document.getElementById('is_CCTV').value;
if (ch6 =="N"){
  document.getElementById('is_CCTV').value="Y";
   }
else if (ch6=='Y'){
  document.getElementById('is_CCTV').value= 'N';
 }        
     
}
function showAdd7(){
var ch7 = document.getElementById('is_Daycare').value;
if (ch7 =="N"){
  document.getElementById('is_Daycare').value="Y";
   }
else if (ch7=='Y'){
  document.getElementById('is_Daycare').value= 'N';
 }             
}
function showAdd8(){
var ch8 = document.getElementById('is_After_School').value;
if (ch8 =="N"){
  document.getElementById('is_After_School').value="Y";
   }
else if (ch8=='Y'){
  document.getElementById('is_After_School').value= 'N';
 }                
}
function showAdd9(){
var ch9 = document.getElementById('is_Residential').value;
if (ch9 =="N"){
  document.getElementById('is_Residential').value="Y";
   }
else if (ch9 =='Y'){
  document.getElementById('is_Residential').value= 'N';
 }              
}


  //===============Affiliates Slideshow =================/

// Next/previous controls
function plusSlides(slideNumber, slideShowNumber) 
{  
  slideIndex[slideShowNumber] += slideNumber;
  showSlides(slideIndex[slideShowNumber], slideShowNumber);
}

// Thumbnail image controls
function currentSlide(slideNumber, slideShowNumber) 
{
    
   slideIndex[slideShowNumber] =  slideNumber;
  showSlides(slideIndex[slideShowNumber], slideShowNumber);
}

function showSlides(slideNumber, slideShowNumber) {
  var i;
    
  var slideshowName = "slider" + slideShowNumber;
    //alert('slideshowName = '+ slideshowName);
  var slides = document.getElementsByName(slideshowName);    
  
    //alert(slides.length);

  var dotname = "dot" + slideShowNumber;
  var dots = document.getElementsByName(dotname);
    
    //alert('slideNumber = '+slideNumber);
  if (slideNumber > slides.length) 
  {
      slideIndex[slideShowNumber] = 1;
  }
  if (slideNumber < 1) 
  {
      slideIndex[slideShowNumber] = slides.length;
    //alert('slideIndex before'+ slideIndex);
  }
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  //alert('slideIndex = '+ slideIndex[slideShowNumber]);
  slides[slideIndex[slideShowNumber]-1].style.display = "block";
  dots[slideIndex[slideShowNumber]-1].className += " active";
}

