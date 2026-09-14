//// testbench - tx-qpsk - PRBS9 - Filtro FIR RC - diezmador y decisor
//defino la escala del tiempo
`timescale 1ns/100ps

module tb_top ();
//parametros 
    parameter NB_SW  = 4;
    parameter NB_LED = 4;
    parameter seed_Q = 9'h1FE;
    parameter seed_I = 9'h1AA;

    parameter OS    = 4;       
    parameter NBAUD = 6;        
    parameter NTAPS = 24;       
    parameter NB_h  = 8;       
    parameter NB_adder = 11;   
    parameter NB_y = 10; 

    parameter NB_count_ber = 64;    
    parameter BER_TH = 30;    

//defino los puertos de entrada (reg) y salida (wire)
    wire    [NB_LED - 1 : 0] o_led   ;

    reg     [NB_SW - 1 : 0] i_sw      ;
    reg     i_rst                     ;   //Reset de la placa activo alto
    reg     clock                     ;    // tiempo de muestro Ts

//inicio el compartamiento
initial begin
    //inicio entradas 
    clock = 1'b0  ;
    i_rst = 1'b0  ;
    i_sw = 4'b0000;

    //defino comportamiento
    #500;                   //Mantengo el reset en 0 durante 500ns para purgar el sistema
    @(posedge clock)          
    i_rst=1'b1;
    #500;                    //Mantego el led en 0 durante 500ns
    @(posedge clock)
    i_sw=4'b0011;              //habilito el sistema de Tx yde Rx - BER , sec de offset 0 3 2 1 0
    #100; 
    @(posedge clock)
    i_sw=4'b0011;              //habilito el sistema de Rx - BER y mantengo el offset en 0
    #10000;
   

    $finish;
end

//construyo el clock
    always #10 clock= ~clock;       //espero 10ns luego conmuto el clk

//instancio el top level
    top
    //Parametros
    #(
        .NB_SW      (NB_SW      ),
        .NB_LED     (NB_LED     ),
        .seed_Q     (seed_Q     ),
        .seed_I     (seed_I     ),

        .OS             (OS             ),        
        .NBAUD          (NBAUD          ),        
        .NTAPS          (NTAPS          ),       
        .NB_h           (NB_h           ),       
        .NB_adder       (NB_adder       ),   
        .NB_y           (NB_y           ),
        .NB_count_ber   (NB_count_ber   ),    
        .BER_TH         (BER_TH         ) 
    )

    u_top
    (
        .o_led  (o_led      ),
        .i_sw   (i_sw       ),
        .i_rst  (i_rst      ),   
        .clock  (clock      )
    );

endmodule