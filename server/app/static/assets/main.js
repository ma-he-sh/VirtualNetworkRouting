(function($){
    console.log("---loaded---");

    const app_nodes = "#app--nodes";
    const app_nodes_comb = "#app--nodes--comb";
    const prop_relation = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-right"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>`;

    var nodes = [];
    var node_index = 0
    var wordList = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    var save_combo=[];

    function update_node_list( letter ) {
        $( app_nodes ).append( "<div class='app--node'>"+letter+"</div>" );
        $( app_nodes_comb ).html('');
        render_combinations();
    }

    function render_combo( prop1, prop2 ) {
        $( app_nodes_comb ).append( 
            `<div class="app--comb">
                <div class="prop-1">${prop1}</div>
                <div class="prop-1">${prop_relation}</div>
                <div class="prop-2">${prop2}</div>
                <div class="prop--cost">
                    <input type="number" data-prop-comb='comb' data-prop1='${prop1}' data-prop2='${prop2}' class="prop--value" value='' />
                </div>
            </div>` 
        );
    }

    function render_combinations() {
        var combo = [];
        if( nodes.length > 1 ) {
            nodes.forEach((prop1, index1) => {
                nodes.forEach((prop2, index2) => {
                    if( prop1 != prop2 ) {
                        var _type1 = prop1 + "" + prop2;
                        var _type2 = prop2 + "" + prop1;

                        if( !(combo.includes(_type1)) && !(combo.includes(_type2)) ) {
                            render_combo(prop1, prop2);
                        }

                        combo.push(_type1);
                        combo.push(_type2);
                    }
                });
            });
        }
    }

    $( "div#app--add-node" ).on("click", function() {
        var letter = wordList.charAt(node_index);
        nodes.push(letter);

        // render nodes
        update_node_list( letter );

        node_index+=1;
    });

    $( "div#app--create-deploy" ).on("click", function() {
        save_combo = [];
        if( nodes.length > 1 ) {
            $('[data-prop-comb]').each(function() {
                save_combo.push({
                    'node1': $(this).data("prop1"),
                    'node2': $(this).data("prop2"),
                    'cost' : parseInt( $(this).val() ),
                });

                console.log( save_combo );
            });
        } else {
            console.error("Invalid Node Size");
        }
    });





















    $( "button[data-action]" ).on("click", function() {
        var _action = $(this).data("action")
        switch( _action ){
            case "create_node":
                create_node()
                break
            case "reset_data":
                nodes = []
                break
            case "deploy_nodes":
                deploy_nodes()
                break
            default:
                print("no action")
        }
    });

    function rest( url, type, data={} ) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,
                type: type,
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: resolve,
                error: reject
            })
        });
    }

    function create_node() {
        var node_cost = parseInt( $('input[name="node_cost"]').val() );
        var node_name = $('input[name="node_name"]').val();
        if (node_cost && node_name) {
            nodes.push({
                "cost": node_cost,
                "name": node_name
            });
            console.log(nodes)
        }
    }

    async function deploy_nodes() {
        if( nodes.length > 0 ) {
            rest( "/deploy_nodes", "post", {
                "nodes": nodes
            } ).then(function(res) {
                console.log(res)
            }).catch(function(err) {
                console.log(err)
            }).finally(function() {
                nodes = [] // clear
            })
        }
    }
})(jQuery);