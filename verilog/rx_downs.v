//Downsample + decisor
module rx_downs
#(
    parameter OS        = 4,
    parameter NB_DATA   = 11
)
(
    output wire                     o_data,   //salida decisor
    output reg                      o_valid,    //Indica que se tomo una muestra y[n]

    input wire        [1:0]         dec_phase,  //se conecta a sw[3:2]
    input wire signed [NB_DATA-1:0] i_data,     //se conecta a la salida del filtro fir
    input wire                      EnbTx,      //se conecta a sw[0]
    input wire                      i_rst,
    input wire                      clock 
);

//Señales internas
    reg         [1:0]           dec_count;       // toma una muestra cada OS-1=3
    reg         [1:0]           offset;          // muestreo, para elejir la posición del ojo 
    reg         [1:0]           aux_phase_reg;
    reg signed  [NB_DATA-1:0]   y_d;            //salida del filtro diezmada yd[n]
    wire                        o_decisor;      //salida del decisor
    reg                         first_sample;
  

//Diezmado
    always @(posedge clock or posedge i_rst) begin
        if (i_rst) begin
            dec_count       <= 2'd0;
            offset          <= dec_phase;
            aux_phase_reg   <= dec_phase;
            y_d             <= {NB_DATA{1'b0}};
            o_valid         <= 1'b0;
            first_sample    <= 1'b0;
     
        end
        else if (EnbTx)  begin                     
            
            if (dec_phase != aux_phase_reg) begin       // Si cambian los switches, se actualiza el offset inicial
                offset          <= dec_phase;             //leo el offset
                aux_phase_reg   <=dec_phase;
                dec_count       <= 2'd0;
                first_sample    <= 1'b0;                  //Vuelvo al estado inicial solo cuando cambia el sw
            end

            else if (first_sample == 1'b0)begin
                if (dec_count == offset) begin          
                    y_d         <= i_data;              //Despues del retardo tomo la 1er muestra     
                    o_valid     <= 1'b1;               //indica que se tomo una muestra      
                    dec_count   <= 2'b0;               //reinicio el contador
                    first_sample<= 1'b1;               //paso al siguiente estado
                end
                else begin
                    o_valid     <= 1'b0;
                    dec_count   <= dec_count + 1;
                    end
            end
            
            else  begin
                if (dec_count == (OS-1)) begin
                    y_d      <= i_data;                     //despues de 3 ciclos tomo una muestra         
                    o_valid  <= 1'b1;               
                    dec_count<=1'b0;               
                end
                else begin
                    o_valid <= 1'b0;
                    dec_count   <= dec_count + 1;
                end
            end
        end
    end

//Decisor
assign o_decisor = (y_d[NB_DATA-1] == 1'b0)? 1'b0 : 1'b1;   //si el bit MSB es 0 entonces es positivo

//BER

//salida
assign o_data = o_decisor;

endmodule