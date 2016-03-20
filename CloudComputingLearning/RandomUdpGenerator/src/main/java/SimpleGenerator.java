/**
 * Created by askofen on 19.03.16.
 */
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.URL;
import java.time.LocalDateTime;
import java.util.Random;
import java.util.Scanner;

public class SimpleGenerator {
    private static String messageFromConsole = null;

    public static void main(String args[]) throws Exception
    {
        if (args == null || args.length < 2)
        {
            System.out.println("Ip address and prot need to be defined in arguments!");
            return;
        }

        String ip = args[0];
        int port = Integer.parseInt(args[1]);

        DatagramSocket clientSocket = new DatagramSocket();
        try {
            InetAddress IPAddress = InetAddress.getByName(ip);
            Random random = new Random();
            Thread consoleThread = new Thread(new ConsoleInput());
            consoleThread.start();

            while (true){
                String message = Integer.valueOf(random.nextInt(1000)).toString();

                if (SimpleGenerator.messageFromConsole != null){
                    message = SimpleGenerator.messageFromConsole;
                    SimpleGenerator.messageFromConsole = null;

                    if (message.equals("exit")){
                        return;
                    }
                }

                message = LocalDateTime.now() + ": " + message;
                byte[] sendData = message.getBytes();
                DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, port);
                clientSocket.send(sendPacket);

                Thread.sleep(1000);
            }
        } catch (Exception e){
            System.out.println(e.getMessage());
        }
        finally {
            clientSocket.close();
        }
    }

    public static class ConsoleInput implements Runnable {
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
