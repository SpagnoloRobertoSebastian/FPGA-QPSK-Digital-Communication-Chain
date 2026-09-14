module top
//Parametros 
#(
    parameter NB_SW  = 4,
    parameter NB_LED = 4,
    parameter seed_Q = 9'h1FE,
    parameter seed_I = 9'h1AA,

    parameter OS    = 4,        
    parameter NBAUD = 6,        
    parameter NTAPS = 24,       
    parameter NB_h  = 8,       
    parameter NB_adder = 11,   
    parameter NB_y = 10,

    parameter NB_count_ber = 64,    //N bits para los contadores de error y total de bits (BER)
    parameter BER_TH = 30          //umbral para la sincronizacion del contador BER
)
//Puertos
(
    output [NB_LED - 1 : 0] o_led   ,

    input [NB_SW - 1 : 0] i_sw      ,
    input i_rst                     ,   //Reset de la placa activo alto
    input clock                         // tiempo de muestro Ts
);

//Señales internas
wire                              o_bits_I;
wire                              o_bits_Q;
wire signed [NB_y   -   1  : 0]   o_fir_I;
wire signed [NB_y   -   1  : 0]   o_fir_Q;
wire                              valid_I;           //la señales internas que se conectan a una salida debe ser tipo wire
wire                              valid_Q;
wire                              yd_decisor_I;        //salida del diezmado
wire                              yd_decisor_Q;  
wire                              led_ber;           // indica si el error es 0
wire                              led_ber_I;    
wire                              led_ber_Q; 
//VIO
wire                              selMux;
wire                              reset_from_VIO;
wire        [NB_SW - 1 : 0]       sw_from_VIO;
wire        [NB_SW - 1 : 0]       sw_V;
wire                              reset_V;   

//Instanciar modulos
// *******************************************************************************//
//                          Canal I
// *******************************************************************************//
prbs9
    #(
        .seed (seed_I)
    )
u_prbs9_I
    (
        .lfsr   (o_bits_I   ),  
        .EnbTx  (sw_V[0]    ),                   
        .i_rst  (reset_V    ),         //internamente es activo alto        
        .clock  (clock      )
);

fir_polyf
#(
    .OS      (OS        ),     
    .NBAUD   (NBAUD     ),        
    .NTAPS   (NTAPS     ),       
    .NB_h    (NB_h      ),       
    .NB_adder(NB_adder  ),   
    .NB_y    (NB_y      )  
)
u_firpoy_I
(
    .o_yn   (o_fir_I    ),     
    .i_xn   (o_bits_I   ),                            
    .EnbTx  (sw_V[0]    ),                            
    .i_rst  (reset_V     ),                           
    .clock  (clock      )
);

rx_downs
#(
    .OS      (OS        ),
    .NB_DATA (NB_y      )
)
u_rx_downs_I
(
    .o_data     (yd_decisor_I ),
    .o_valid    (valid_I    ),
    .dec_phase  (sw_V[3:2]  ),
    .i_data     (o_fir_I    ),
    .EnbTx      (sw_V[0]    ),
    .i_rst      (reset_V     ),
    .clock      (clock      )
);

ber_count
#(
    .NB_COUNT    (NB_count_ber  ),   
    .SEED        (seed_I        ),   
    .SYNC_THR    (BER_TH        ) 
)
u_ber_count_I
(
    .o_led_ber      (led_ber_I        ),      
    .i_valid        (valid_I        ),          
    .i_rx_bit       (yd_decisor_I   ),         
    .EnvRx          (sw_V[1]        ),           
    .i_rst          (reset_V         ),
    .clock          (clock          )
);
// *******************************************************************************//
//                          Canal Q
// *******************************************************************************//
//Canal Q
prbs9
    #(
       .seed (seed_Q)
   )
u_prbs9_Q
    (
       .lfsr   (o_bits_Q   ),  
        .EnbTx (sw_V[0]    ),                   
       .i_rst  (reset_V     ),                 
        .clock (clock      )
);

fir_polyf
#(
    .OS      (OS        ),     
    .NBAUD   (NBAUD     ),        
    .NTAPS   (NTAPS     ),       
    .NB_h    (NB_h      ),       
    .NB_adder(NB_adder  ),   
    .NB_y    (NB_y      )  
)
u_firpoy_Q
(
    .o_yn   (o_fir_Q    ),     
    .i_xn   (o_bits_Q   ),                            
    .EnbTx  (sw_V[0]    ),                            
    .i_rst  (reset_V     ),                           
    .clock  (clock      )
);

rx_downs
#(
    .OS      (OS        ),
    .NB_DATA (NB_y      )
)
u_rx_downs_Q
(
    .o_data     (yd_decisor_Q ),
    .o_valid    (valid_Q    ),
    .dec_phase  (sw_V[3:2]  ),
    .i_data     (o_fir_Q    ),
    .EnbTx      (sw_V[0]    ),
    .i_rst      (reset_V     ),
    .clock      (clock      )
);

ber_count
#(
    .NB_COUNT    (NB_count_ber  ),   
    .SEED        (seed_Q        ),   
    .SYNC_THR    (BER_TH        ) 
)
u_ber_count_Q
(
    .o_led_ber      (led_ber_Q    ),      
    .i_valid        (valid_Q    ),          
    .i_rx_bit       (yd_decisor_Q ),         
    .EnvRx          (sw_V[1]    ),           
    .i_rst          (reset_V     ),
    .clock          (clock      )
);

VIO
u_VIO(
    .clk_0       (clock),
    .probe_in0_0 (o_led),
    .probe_out0_0(selMux),
    .probe_out1_0(reset_from_VIO),
    .probe_out2_0(sw_from_VIO)
);
// MUX para el VIO
//Si el selMux=1 conecto la salida del Mux con la ent sw_from_VIO, sino lo conecto a i_sw entradas de la placa
   assign sw_V      = (selMux) ? sw_from_VIO : i_sw;
// MUX reset VIO
//Si el selMux=1 conecto la salida del Mux con la ent reset_from_VIO, sino lo conecto a i_rst
   assign reset_V   = (selMux) ? ~reset_from_VIO : ~i_rst;

//selMux = 1 selecciono el sw del vio y seleccione el reset del vio 

ILA
u_ILA
(
    .clk_0    (clock),
    .probe0_0 (o_led),
    .probe1_0 (o_fir_I),
    .probe2_0 (o_fir_Q),
    .probe3_0 (yd_decisor_I),
    .probe4_0 (yd_decisor_Q),
    .probe5_0 (valid_I),
    .probe6_0 (valid_Q)
    );


// *******************************************************************************//
//                     Conexión con los puertos de salida
// *******************************************************************************//
   assign led_ber = led_ber_I & led_ber_Q;
   assign o_led[0] = reset_V    ;       //conecto led 0 con el reset
   assign o_led[1] = sw_V[0]    ;       //conecto led 1 con enable TX
   assign o_led[2] = sw_V[1]    ;       //conecto led 2 con enable Rx
   assign o_led[3] = led_ber    ;       //led 3 indica si el error es 0

endmodule