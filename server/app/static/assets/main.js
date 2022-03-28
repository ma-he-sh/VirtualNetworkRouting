class PathGen {
    section="app--proposed--path";
    net_path="app--route--path";

    constructor(start, end, path=[], data=[]) {
        this.start = start;
        this.end   = end;
        this.path  = path;
        this.data  = data;
        this.el = document.getElementById( this.section );
        this.network = null;
    }

    init() {
        console.log("initization");
        this.clear();

        var data = this.calc();
        this.network = new vis.Network( this.el, data, {
            nodes: {
                shape: "dot",
            }
        } );
    }

    calc() {
        var data = {
            nodes: [],
            edges: [],
        }

        var index_map = {}
        var path_map  = {}

        if( this.data.nodes.length > 0 ) {
            this.data.nodes.forEach( function( label, index ) {
                index_map[label] = index;
                data.nodes.push( {
                    id: index,
                    label: label
                } );
            } );
        }

        if( this.data.cost.length > 0 ) {
            this.data.cost.forEach( function( nodes, index ) {
                var node1_index = index_map[nodes.node1];
                var node2_index = index_map[nodes.node2];
                if( !isNaN(nodes.cost) ) {
                    var push_index = data.edges.push({
                        from: node1_index,
                        to: node2_index,
                        value: 2,
                        label: nodes.cost
                    });

                    path_map[ `${nodes.node1}_${nodes.node2}` ] = {
                        index: push_index - 1,
                        cost: nodes.cost
                    }
                }
            } );
        }

        // path handle
        if( this.path.length > 0 ) {
            var path_string = "";
            var combo = [];

            var observer_index = this.path.indexOf("OBSERVER");
            if( observer_index > 0 ) {
                this.path.splice(observer_index, 1);
            }

            var index = 1;
            var start = this.path[0];

            path_string += `${start}`;
            while( index < this.path.length ) {
                var end = this.path[index];

                var from_edge = index_map[start];
                var to_edge   = index_map[end];

                path_string += ` => ${end}`;

                var orignal_index = path_map[ `${start}_${end}` ].index;
                var orignal_cost  = path_map[ `${start}_${end}` ].cost;

                data.edges[orignal_index] = {
                    from: from_edge,
                    to: to_edge,
                    value: 6,
                    label: orignal_cost
                };

                start = end;
                index++;
            }

            // render the path
            jQuery(`#${this.net_path}`).html( path_string );
        }

        console.log( path_map )

        return data;
    }

    clear() {
        jQuery( `#${this.section}` ).html("");
        jQuery( `#${this.net_path}` ).html("");
        jQuery("[data-vis]").removeClass("display--none");
    }
}

(function($){
    console.log("---loaded---");
    var pathgen = null;

    const app_nodes = "#app--nodes";
    const app_nodes_comb = "#app--nodes--comb";
    const prop_relation = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-right"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>`;

    var nodes = [];
    var node_index = 0
    var wordList = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    var save_combo=[];

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
                var cost = parseInt( $(this).val() );
                if ( cost == NaN ) {
                    cost = 0;
                }
                save_combo.push({
                    'node1': $(this).data("prop1"),
                    'node2': $(this).data("prop2"),
                    'cost' : cost,
                });
            });
            
            var data = {
                'cost' : save_combo,
                'nodes': nodes,
            }

            rest( "/deploy_nodes", "post", data ).then(function(res) {
                if( res.hasOwnProperty('code') && res.code == "path_generated" ) {
                    return {
                        'data': data,
                        'start': res.start,
                        'end' : res.end,
                        'path': res.path
                    }
                }
            })
            .then(function(nodes) {
                pathgen = new PathGen( nodes.start, nodes.end, nodes.path, nodes.data );
                pathgen.init();
            })
            .catch(function(err) {
                console.log(err)
            }).finally(function() {
                save_combo = [];
            });
        } else {
            console.error("Invalid Node Size");
            swal("Error : Invalid Node Size", "Something went wrong, please try again", "warning");
        }
    });

    $( "div#app--send-msg" ).on( "click", function() {
        var payload = $( "#send_message" ).val();
        if( payload.length > 0 ) {
            var data = {
                'msg': payload
            }
            rest("/send_packet", "post", data ).then(function(res){
                if( res.sent ) {
                    swal("Packet Sent", "Packet sent successfully", "success")
                    .then(function(res){
                        if(res){
                            $( "#send_message" ).val("");
                        }
                    });
                }
            }).catch(function(err){
                swal("Error: Message Not Sent", "Something went wrong, please try again", "warning");
            }).finally(function() {

            });
        }
    } );

    $( "div#app--reset" ).on("click", function() {
        location.reload();
    });
})(jQuery);
