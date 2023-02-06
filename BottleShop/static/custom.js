//Begin Document.Ready
$(document).ready(function(){

    //All product Load More when load more button is clicked
	$("#loadMore").on('click',function(){
		var _currentProducts=$(".product-box").length;
		var _limit=$(this).attr('data-limit');
		var _total=$(this).attr('data-total');
		var _catid=$(this).attr('data-catid');
		console.log(_currentProducts,_limit,_total);
		// Start Ajax
		$.ajax({
			url:'/load-more-data',
			data:{
				limit:_limit,
				offset:_currentProducts,
				cat_id:_catid
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
			},
			success:function(res){
				$("#filteredProducts").append(res.data);
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');
        //Hide  button after all products are loaded
				var _totalShowing=$(".product-box").length;
				if(_totalShowing>=_total){
					$("#loadMore").remove();
				}
			}
		});
		// EndAjax
	});
    // End All product Load More

    //Category Load More when load more button is clicked
    $("#catloadMore").on('click',function(){
            var _currentProducts=$(".cat-product-box").length;
            var _limit=$(this).attr('data-limit');
            var _total=$(this).attr('data-total');
            var _catid=$(this).attr('data-catid');
            console.log(_currentProducts,_limit,_total,_catid);
            // Start Ajax
            $.ajax({
                url:'/cat-load-more-data',
                data:{
                    limit:_limit,
                    offset:_currentProducts,
                    cat_id:_catid
                },
                dataType:'json',
                beforeSend:function(){
                    $("#catloadMore").attr('disabled',true);
                    $(".cat-load-more-icon").addClass('fa-spin');
                },
                success:function(res){
                    $("#catfilteredProducts").append(res.data);
                    $("#catloadMore").attr('disabled',false);
                    $(".cat-load-more-icon").removeClass('fa-spin');
            //Hide  button after all products are loaded
                    var _totalShowing=$(".cat-product-box").length;
                    if(_totalShowing>=_total){
                        $("#catloadMore").remove();
                    }
                }
            });
		    // EndAjax
		});
    //End Category Load More


    //Brand Load More when load more button is clicked
    $("#brandloadMore").on('click',function(){
            var _currentProducts=$(".brand-product-box").length;
            var _limit=$(this).attr('data-limit');
            var _total=$(this).attr('data-total');
            var _brandid=$(this).attr('data-brandid');
            console.log(_currentProducts,_limit,_total,_brandid);
            // Start Ajax
            $.ajax({
                url:'/brand-load-more-data',
                data:{
                    limit:_limit,
                    offset:_currentProducts,
                    brand_id:_brandid
                },
                dataType:'json',
                beforeSend:function(){
                    $("#brandloadMore").attr('disabled',true);
                    $(".brand-load-more-icon").addClass('fa-spin');
                },
                success:function(res){
                    $("#brandfilteredProducts").append(res.data);
                    $("#brandloadMore").attr('disabled',false);
                    $(".brand-load-more-icon").removeClass('fa-spin');
            //Hide  button after all products are loaded
                    var _totalShowing=$(".brand-product-box").length;
                    if(_totalShowing>=_total){
                        $("#brandloadMore").remove();
                    }
                }
            });
            // EndAjax
		});
    //End Brand Load More


    // Product Variation
	$(".choose-size").hide();
    // Show size and price according to selected color, keep first size active and also show price for first size under selected  color
	$(".choose-color").on('click',function(){
	//Remove active existing color and focused size when particular color is picked and then add current color to be focused
		$(".choose-color").removeClass('focused');
		$(this).addClass('focused');
		$(".choose-size").removeClass('active');
    //Get data-color attribute set in color button
	    var _color=$(this).attr('data-color');
    //Choose-size class is given to all sized, first hide all and then only show the one which has class
    //with the name of 'color appended with actual color attr'
		$(".choose-size").hide();
		$(".color"+_color).show();
	//Following is to show first size for selectedcolor as active  by selecting class build with 'color+_color'
		$(".color"+_color).first().addClass('active');
    //Following is to show price for first size/selectedcolor by selecting data-price attr of first (size)class build with 'color+_color'
		var _price=$(".color"+_color).first().attr('data-price');
		$(".color-size-price").text(_price);

	});
    // End

    // Show the price according to selected size
	$(".choose-size").on('click',function(){
		$(".choose-size").removeClass('active');
		$(this).addClass('active');

		var _price=$(this).attr('data-price');
		$(".color-size-price").text(_price);
	});
    // End

    // Show the first color selected as well as first size whithin the color is focused
	$(".choose-color").first().addClass('focused');
	var _color=$(".choose-color").first().attr('data-color');
	var _price=$(".choose-size").first().attr('data-price');

	$(".color"+_color).show();
	$(".color"+_color).first().addClass('active');
	$(".color-size-price").text(_price);
    //End

    // Add to cart
		//Changed from id #addToCartBtn to havev add to cart functionality available from all pages
	$(document).on('click',".add-to-cart",function(){
		var _vm=$(this);
		var _index=_vm.attr('data-index');
//		var _color =$(".product-color-"+_index).attr("value");
//		var _size =$(".product-size-"+_index).attr("value");
		var _qty=$(".product-qty-"+_index).val();
		var _productId=$(".product-id-"+_index).val();
		var _productImage=$(".product-image-"+_index).val();
		var _productTitle=$(".product-title-"+_index).val();
		var _productPrice=$(".product-price-"+_index).text();
//		console.log(_color,_size,_qty,_productId,_productTitle);
		console.log(_qty,_productId,_productTitle,_productPrice);
		// Ajax
		$.ajax({
			url:'/add-to-cart',
			data:{
//			    'color':_color,
//			    'size':_size,
				'id':_productId,
				'image':_productImage,
				'qty':_qty,
				'title':_productTitle,
				'price':_productPrice
			},
			dataType:'json',
			beforeSend:function(){
            //This will disable add to cart button while add to cart return success
				_vm.attr('disabled',true);
			},
			success:function(res){
           //IN base.html defaault value is set as length to retain it while chaning product, you could  try and removing it to see its going to 0 as soonn
    //as you change the product
				$(".cart-list").text(res.totalitems);
				console.log('*******************');
				console.log(res);
				_vm.attr('disabled',false);
			}
		});
		// EndAjax
	});
	// End

	// Delete item from cart
	$(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// EndAjax
	});
	// End

    // Update item in cart within cart. i.e. using up and down arrow and click on refresh button
	$(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// EndAjax
	});
	// End

	// Check the radio button value.
        $(document).on('click','#btn',function(){
            var _payout=$('input[name=payment_option]:checked',
                '#myForm').val();
            console.log(_payout);

//            document.querySelector(
//              '.output').textContent = output;
        });
    // End

	// Add wishlist
	$(document).on('click',".add-wishlist",function(){
		var _pid=$(this).attr('data-product');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/add-wishlist',
			data:{//Data send to url mentioned above
				product:_pid
			},
			dataType:'json',
			success:function(res){//response received from view
			    console.log(res.bool)
				//if(res.bool==true){
					_vm.addClass('disabled').removeClass('add-wishlist');
				//}
			}
		});
		// EndAjax
	});
	// End

    // Product Review Save
        $("#addForm").submit(function(e){
            $.ajax({
                data:$(this).serialize(),
                method:$(this).attr('method'),//This will get attr of method tag of element with id addForm, you could instead put 'POST'
                url:$(this).attr('action'),//This will get attr of action tag of element with id addForm,
                                            //you could instead use string with product id set as variable using data-item
                dataType:'json',
                success:function(res){
                    if(res.bool==true){
                        $(".ajaxRes").html('Data has been added.');
    //                    $("#reset").trigger('click');
    //Reset form on clicking reset id element, this can be done with above trigger methode as well
                        $(document).ready(function(){
                            $(".reset").click(function(){
                                $("#myForm").trigger("reset");
                            });
                        });
                        // Hide Button after successful review
                        $(".reviewBtn").hide();
                        // End

                        // create data for review
                        var _html='<blockquote class="blockquote text-right">';
                        _html+='<small>'+res.data.review_text+'</small>';
                        _html+='<footer class="blockquote-footer">'+res.data.user;
                        _html+='<cite title="Source Title">';
                        for(var i=1; i<=res.data.review_rating; i++){
                            _html+='<i class="fa fa-star text-warning"></i>';
                        }
                        _html+='</cite>';
                        _html+='</footer>';
                        _html+='</blockquote>';
                        _html+='</hr>';

                        $(".no-data").hide();//Hide paragraph tag "Add First Review"

                        // Prepend Data before existing html element to show latest review on top
                        $(".review-list").prepend(_html);

                        // Hide Modal after review added successfully
                        $("#productReview").modal('hide');

                        // AVg Rating coming from save_review view
                        $(".avg-rating").text(res.avg_reviews.avg_rating.toFixed(1));
                    }
                }
            });
            e.preventDefault();
        });
    // End


	// Activate selected address
	$(document).on('click','.activate-address',function(){
		var _aId=$(this).attr('data-address');// get attr set using in html in addressbook.html with class 'activate_address'
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/activate-address',
			data:{
				'id':_aId,
			},
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					$(".address").removeClass('shadow border-secondary');
					$(".address"+_aId).addClass('shadow border-secondary');

					$(".check").hide();
					$(".actbtn").show();

					$(".check"+_aId).show();
					$(".btn"+_aId).hide();
				}
			}
		});
		// End Ajax
	});

    $(document).ready(function(){
    $(window).on("beforeunload", function(e) {
        $.ajax({
                url: logout,
                method: 'GET',
            })
    });
});
});
// End Document.Ready

