/**
 * Created by askofen on 19.03.16.
 */
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.time.LocalDateTime;
import java.util.Random;
import java.util.Scanner;

public class SimpleGenerator {
    private static String messageFromConsole = null;

    public static void main(String args[]) throws Exception
    {
        if (args == null || args.length < 2)
        {
            System.out.println("Ip address and port need to be defined in arguments!");
            return;
        }

        String ip = args[0];
        int port = Integer.parseInt(args[1]);

        int delay = 1000;
        if (3 <= args.length)
            delay = Integer.parseInt(args[2]);

        DatagramSocket clientSocket = new DatagramSocket();

        try {
            InetAddress IPAddress = InetAddress.getByName(ip);
            Random random = new Random();
            Thread consoleThread = new Thread(new ConsoleInput());
            consoleThread.start();
            System.out.println("Connected to: " + ip + ":" + port);

            int valueIncrement = 0;

            while (true){

                if (SimpleGenerator.messageFromConsole != null){
                    String input = SimpleGenerator.messageFromConsole;
                    SimpleGenerator.messageFromConsole = null;

                    if (input.equals("exit")){
                        return;
                    }

                    try {
                        valueIncrement = Integer.parseInt(input);
                    }
                    catch (NumberFormatException e){
                    }
                }

                Integer val1 = Integer.valueOf(random.nextInt(200)) - 100 + valueIncrement;
                Integer val2 = Integer.valueOf(random.nextInt(200)) - 100;
                Integer val3 = Integer.valueOf(random.nextInt(200)) - 100;

                String message1 = "Sensor1 " + val1 + " ";
                String message2 = "Sensor2 " + val2 + " ";
                String message3 = "Sensor3 " + val3 + " ";

                SendMessage(message1, IPAddress, port, clientSocket);
                SendMessage(message2, IPAddress, port, clientSocket);
                SendMessage(message3, IPAddress, port, clientSocket);

                Thread.sleep(delay);
            }
        } catch (Exception e){
            System.out.println(e.getMessage());
        }
        finally {
            clientSocket.close();
        }
    }

    private static void SendMessage(String message, InetAddress IPAddress, int port, DatagramSocket clientSocket) throws IOException {
        String prefix = LocalDateTime.now() + " ";
        String messageToSend = prefix + message;

        byte[] sendData = messageToSend.getBytes();
        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, port);
        clientSocket.send(sendPacket);
        System.out.println("Message sent: " + messageToSend);
    }

    private static class ConsoleInput implements Runnable {
        public void run() {
            Scanner sc = new Scanner(System.in);

            while (true) {
                String message = sc.nextLine();
                SimpleGenerator.messageFromConsole = message;

                if (message.equals("exit"))
                    return;
            }
        }
    }
}
