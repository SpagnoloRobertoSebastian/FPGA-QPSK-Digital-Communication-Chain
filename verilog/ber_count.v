module ber_count
#(
    parameter NB_COUNT = 64,        // Tamaño de los contadores para evitar overflow
    parameter SEED     = 9'h1AA,    // Semilla para el canal I (debe ser igual a la del Tx)
    parameter SYNC_THR = 31         // Umbral: cantidad de bits seguidos sin error para declarar sincronismo
)
(
    output reg o_led_ber,           //enciende led 3 si el error se mantiene en 0

    input wire i_valid,          // Pulso en alto (1 ciclo) cuando hay un bit nuevo
    input wire i_rx_bit,         // Bit recibido desde el decisor
    input wire EnvRx,           //habilito el ber count se conecta a sw[1] y salida led[2]
    input wire i_rst,
    input wire clock
    
);

    // Señales internas
    wire prbs_bit;                  // Bit generado por la PRBS local
    wire prbs_en;                   // Habilitación de la PRBS local
    wire bit_match;                 // Bandera de coincidencia
    
    reg [5:0] match_count;           // Contador integrador para buscar sincronismo (hasta 63)
    reg [NB_COUNT-1:0] o_total_bits; // Contador total de bits 
    reg [NB_COUNT-1:0] o_error_bits; // Contador de bits erróneos
    reg  o_sync_search;             // Indicador de sincronismo (1 = sincronizado, 0 = Buscando) se conecta a led[3]

    //Instancia de la PRBS9 local

    prbs9 #(
        .seed(SEED)
    ) u_prbs9_local (
        .lfsr  (prbs_bit),
        .EnbTx (prbs_en),
        .i_rst (i_rst), 
        .clock (clock)
    );

    // Comparación 
    // comparo si hay conicidencia entre el bit Rx y el bit de la PRBS9 local
    assign bit_match = (i_rx_bit == prbs_bit);

   
    //durante la busqueda de sincronismo habilito la prbs9 siempre que haya coincidencia
    //sino retraso la prbs9 local un ciclo de clock
    assign prbs_en = i_valid & (o_sync_search | bit_match);

    // Control - Máquina de Estados     
    always @(posedge clock or posedge i_rst) begin:Control
        if (i_rst) begin
            o_sync_search<= 1'b0;
            match_count  <= 6'd0;
            o_led_ber    <= 1'b0;
            o_total_bits <= {NB_COUNT{1'b0}};
            o_error_bits <= {NB_COUNT{1'b0}};
        end
        else if (i_valid==1 && EnvRx==1) begin
            
            // estado 1: buscando sincronismo
            if (!o_sync_search) begin
                if (bit_match) begin
                    // Si coincide, sumamos al integrador
                    if (match_count == SYNC_THR) begin
                        o_sync_search <= 1'b1;  // hay sincronismo, paso al proximo estado
                        match_count <= 6'd0;
                    end
                    else begin
                        match_count <= match_count + 6'd1;
                    end
                end
                else begin
                    // Si falla un bit antes de llegar al umbral, se resetea la búsqueda
                    match_count <= 6'd0; 
                end
            end
            
            // estado 2: bit Rx y bit local sincronizado, detecto el error (ber)
            else begin
                o_total_bits <= o_total_bits + 64'd1;
                
                if (!bit_match) begin
                   o_error_bits <= o_error_bits + 64'd1;
                   o_led_ber<=1'b0;
                end
                else begin
                    o_led_ber<=1'b1;
                end
            end
        end
    end

endmodule

