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
    i_sw=4'b0001;              //habilito el sistema de Tx, sec de offset 0 3 2 1 0
    #1000; 
    @(posedge clock)
    i_sw=4'b0101;              // sec de offset=1 -> fase 1, 0, 3, 2, 1 ..
    #1000;
    @(posedge clock)
    i_sw=4'b0001;              //sec de offset=0 -> 0 3 2 1 0
    #1000;
    @(posedge clock)
    i_sw=4'b1001;              //sec de offset=2 -> fase 2, 1, 0, 3, 2, ..
    #1000;
     @(posedge clock)
    i_sw=4'b1101;              //sec de offset=3 -> fase  3, 2, 1, 0, 3, ..
    #1000;

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

        .OS         (OS         ),        
        .NBAUD      (NBAUD      ),        
        .NTAPS      (NTAPS      ),       
        .NB_h       (NB_h       ),       
        .NB_adder   (NB_adder   ),   
        .NB_y       (NB_y       )
    )

    u_top
    (
        .o_led  (o_led      ),
        .i_sw   (i_sw       ),
        .i_rst  (i_rst      ),   
        .clock  (clock      )
    );

endmodule