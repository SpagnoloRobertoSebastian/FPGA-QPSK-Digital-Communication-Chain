module prbs9
//parameters
#(
    parameter seed = 9'h1FE         //semilla para Q
) 
// ports
(
   output lfsr  ,

   input  EnbTx ,                    //enable i_sw[0]
   input  i_rst ,                    //Reset asincronico activo alto
   input  clock                     // tiempo de muestro Ts
);

//Señales internas
reg [8 : 0] shiftreg;
wire        feedback;

assign feedback = shiftreg[8] ^ shiftreg[4];

always @(posedge clock or posedge i_rst) begin
    if (i_rst) begin
        shiftreg <= seed;
    end
    
    else if (EnbTx) begin
//Uso la concatenacion para guardar el resultado de la XOR en el MSB y desplazo hacia la derecha
        shiftreg <= {feedback, shiftreg[8:1]};            
    end
end
//Conexion puertos de salida    
assign lfsr = shiftreg[0];
endmodule